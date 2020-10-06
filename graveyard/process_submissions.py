import pandas as pd
import re
import datetime as dt
import csv
import glob
from os import listdir
from os.path import isfile, join

# Start date = date that r/trp was created
start = dt.datetime.strptime('2012-10-25', '%Y-%m-%d').date()

# End date = date that r/trp was quarantined
end = dt.datetime.strptime('2018-09-01', '%Y-%m-%d').date()


def clean_subreddit(filename):
    """Cleans the file passed in.
    Saves files to processed/submissions folder within trpred."""

    # Get name for processed file
    regex = r"([^\/]+)(?=\-all)"
    matches = re.search(regex, subreddit_folder)
    new_file = matches.group(1)

    # Create list of columns to keep
    keep_cols = ['id', 'created_utc', 'author', 'title',\
                  'score', 'num_comments', 'subreddit', 'link_flair_text']

    keep_cols_text = ['id', 'created_utc', 'author', 'selftext']

    # Create file name
    processedfile_csv = "data/processed/submissions/" + new_file + \
        "-metadata" +  ".csv"

    processed_textfile_csv = "data/processed/submissions/" + new_file + \
        "-text" + ".csv"

    # Create empty data frame
    df_keep = pd.DataFrame()
    df_keep_text = pd.DataFrame()

    # Read in json file
    try:
        data = pd.read_json(filename)

    # ValueError: Trailing data thrown if file is pretty indented
    except ValueError:
        data = pd.read_json(filename, lines = True)

    try:
        df_keep = df_keep.append(data[keep_cols])
    except KeyError:
        keep_cols = ['id', 'created_utc', 'author', 'title',\
                    'score', 'num_comments', 'subreddit']
        df_keep = df_keep.append(data[keep_cols])

    try:
        df_keep_text = df_keep_text.append(data[keep_cols_text])
    except KeyError:
        keep_cols_text = ['id', 'created_utc', 'author']
        df_keep_text = df_keep_text.append(data[keep_cols_text])


    # Change date format
    ## For metadata
    df_keep['datetime_dv'] = pd.to_datetime(df_keep['created_utc'], unit = 's')# dv = derived
    df_keep['date_dv'] = df_keep['datetime_dv'].dt.date

    # For text
    df_keep_text['datetime_dv'] = pd.to_datetime(df_keep_text['created_utc'], unit = 's')# dv = derived
    df_keep_text['date_dv'] = df_keep_text['datetime_dv'].dt.date


    ##### Delimit by date #####
    # Create mask of time slot
    mask = (df_keep['date_dv'] >= start) & (df_keep['date_dv'] <= end) # inclusive on either end
    mask_text = (df_keep_text['date_dv'] >= start) & (df_keep_text['date_dv'] <= end)

    # Only keep data within date frame
    df_keep = df_keep.loc[mask]
    df_keep_text = df_keep_text.loc[mask_text]
    ############################


    # Save to json
    df_keep_text.to_csv(processed_textfile_csv, mode = "w")
    df_keep.to_csv(processedfile_csv, mode = "w") # mode= w will overwrite previous file
    print(len(df_keep_text.index))
    print(processed_textfile_csv)


    data = [] # force empty


class process_submissions():
    def __init__(self, parent_folder):
        subreddit_files = glob.glob(parent_folder+"/*.json")
