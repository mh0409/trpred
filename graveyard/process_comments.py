import pandas as pd
import re
import utils
import datetime as dt
import csv
import os
from os import listdir
from os.path import isfile, join
from fsplit.filesplit import FileSplit
import clean
import glob

def clean_comments(subreddit_folder):
    """Cleans comments found in the folder passed in."""

    # Get name for processed file
    regex = r"([^\/]+)(?=\-all)"
    matches = re.search(regex, subreddit_folder)
    new_file = matches.group(1)

    # Comment files
    files = [f for f in listdir(subreddit_folder) if isfile(join(subreddit_folder, f))]

    # Create list of columns to keep
    keep_cols = ['id', 'created_utc','author',\
                  'author_flair_text', 'score', 'parent_id',\
                  'subreddit']
    keep_cols_text = ['id', 'created_utc', 'parent_id', 'body']

    # Create file name
    processedfile_csv = "data/processed/comments/" + new_file + \
        "-metadata" +  ".csv"

    processed_textfile_csv = "data/processed/comments/" + new_file + \
        "-text" + ".csv"

    counter = 0

    # Read in json file
    for i in files:
        print(i)
        counter += 1

        df_keep = pd.DataFrame()
        df_keep_text = pd.DataFrame()

        file_path = subreddit_folder + "/" + i

        try:
            data = pd.read_json(file_path)

        # ValueError: Trailing data thrown if file is pretty indented
        except ValueError:
            data = pd.read_json(file_path, lines = True)


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

        # Make sure there's at least 1 observation
        observations = len(df_keep.index)

        # Change date format
        ## For metadata
        if observations == 0:
            print("No comments found in " + i)
            continue

        else:
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

        # Save to csv
        if counter == 1:
            df_keep.to_csv(processedfile_csv, mode = "w")
            df_keep_text.to_csv(processed_textfile_csv, mode = "w")

        else:
            df_keep.to_csv(processedfile_csv, mode = "a", header = False)
            df_keep_text.to_csv(processed_textfile_csv, mode = "a", header = False)



class process_comments():
    def __init__(self, parent_folder):
        subreddit_folders = [x[0] for x in os.walk(parent_folder)]
        process_comments.subreddit_folders = subreddit_folders[1:] # item at index 0 is parent folder so exclude
