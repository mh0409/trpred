#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:43:47 2020

@author: mariajoseherrera
"""

import pandas as pd
import re
import datetime as dt
import csv

# Start date = date that r/trp was created
start = dt.datetime.strptime('2012-10-25', '%Y-%m-%d').date()

# End date = date that r/trp was quarantined
end = dt.datetime.strptime('2018-09-01', '%Y-%m-%d').date()


def clean_subreddit(filename, data_type):
    """Cleans the file passed in as the first argument based on data type.
    Data_type takes values "submmissions" or "comments", else throws ValueError;
    this determines the columns to be kept in the corresponding data frame.
    Saves files to processed/submissions folder within trpred.
    Returns the column headers we can expect to see in the saved file."""

    ## MAYBE REPLACE FILENAMES WITH SUBREDDIT AND MOVE GLOB INTO HERE
    ## or split into clean comments and clean submissions since comments are so much bigger


    # Get date for filename
    today = dt.datetime.utcnow().date()

    regex = r"([^\/]+)(?=\.json$)"
    matches = re.search(regex, filename)
    new_file = matches.group()

    if data_type == "submissions":
        # Create list of columns to keep
        keep_cols = ['id', 'created_utc', 'author', 'title',\
                      'score', 'num_comments', 'subreddit', 'link_flair_text']

        keep_cols_text = ['id', 'created_utc', 'author', 'selftext']

        # Create file name
        processedfile_csv = "data/processed/submissions/" + new_file + \
            "-metadata" +  ".csv"

        processed_textfile_csv = "data/processed/submissions/" + new_file + \
            "-text" + ".csv"

    elif data_type == "comments":
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

    else:
        raise ValueError("Unsupported data_type. 'data_type' only takes values\
                          'submissions' or 'comments'")

    df_keep = pd.DataFrame()
    df_keep_text = pd.DataFrame()

    # for file in filename:

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
    # TODO: break this out into different function
    # Create mask of time slot
    mask = (df_keep['date_dv'] >= start) & (df_keep['date_dv'] <= end) # inclusive on either end
    mask_text = (df_keep_text['date_dv'] >= start) & (df_keep_text['date_dv'] <= end)

    # Only keep data within date frame
    df_keep = df_keep.loc[mask]
    df_keep_text = df_keep_text.loc[mask_text]
    ############################


    # Save to json
    df_keep.to_csv(processedfile_csv, mode = "w") # mode= w will overwrite previous file
    df_keep_text.to_csv(processed_textfile_csv, mode = "w")
    print(len(df_keep.index))


    data = [] # force empty


    return keep_cols

## TODO: update so that i'm adding to comment file in the same way i scrape it for the big r/TRP scrape
# with open(processedfile_csv, 'a', encoding = 'utf-8') as fp:
#         json.dump(obj.d_, fp, ensure_ascii = False) # write file
#         fp.write('\n')
