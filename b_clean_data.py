
import pandas as pd
import re
import utils
import datetime as dt
import csv
import os
from os import listdir
from os.path import isfile, join
from fsplit.filesplit import FileSplit
import glob

def clean_comments(raw_comments):
    """Cleans comments found in the folder passed in."""

    # Create one folder for each subreddit, containing 15MB chunks of the raw file
    new_folder = utils.create_folder(raw_comments, "comments")

    # Don't need this -- will return path anyways
    # if new_folder == None:
    #     print("No directory created")
    #     new_folder = "data/raw/comments/" + utils.get_filename(raw_comments)

    # Create list of comment files
    files = [f for f in listdir(new_folder) if isfile(join(new_folder, f))]
    print(*files, sep = "\n")

    # Get name for processed file
    regex = r"([^\/]+)(?=.allcomments)"
    matches = re.search(regex, raw_comments)
    new_file = matches.group(1)



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

    counter = 0 # set up counter to determine whether to write or append to file

    # Read in json file
    for i in files:
        counter += 1

        df_keep = pd.DataFrame()
        df_keep_text = pd.DataFrame()

        file_path = new_folder + "/" + i

        try:
            data = pd.read_json(file_path)

        # ValueError: Trailing data thrown if file is pretty indented
        except ValueError:
            data = pd.read_json(file_path, lines = True)


        try:
            df_keep = df_keep.append(data[keep_cols])
        except KeyError:
            keep_cols = ['id', 'created_utc', 'author', 'title',\
                        'score', 'num_comments', 'subreddit'] # relevant comment columns
            df_keep = df_keep.append(data[keep_cols])


        try:
            df_keep_text = df_keep_text.append(data[keep_cols_text])
        except KeyError:
            keep_cols_text = ['id', 'created_utc', 'author']
            df_keep_text = df_keep_text.append(data[keep_cols_text])

        # Make sure there's at least 1 observation
        observations = len(df_keep.index)

        # If there are no observations, move to next subreddit
        if observations == 0:
            print("No comments found in " + i)
            continue

        # Change date format
        ## For metadata
        else:
            df_keep['datetime_dv'] = pd.to_datetime(df_keep['created_utc'], unit = 's')# dv = derived
            df_keep['date_dv'] = df_keep['datetime_dv'].dt.date

            # For text
            df_keep_text['datetime_dv'] = pd.to_datetime(df_keep_text['created_utc'], unit = 's')# dv = derived
            df_keep_text['date_dv'] = df_keep_text['datetime_dv'].dt.date


        ##### Delimit by date #####
        start = dt.datetime.fromtimestamp(utils.get_startdate()).date()
        end = dt.datetime.fromtimestamp(utils.get_enddate()).date()

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




# def clean_submissions(raw_submissions):
#     """Cleans the file passed in.
#     Saves files to processed/submissions folder within trpred."""
#
#     # Create one folder for each subreddit, containing 15MB chunks of the raw file
#     new_folder = utils.create_folder(raw_submissions, "submissions")
#
#     # Create list of comment files
#     files = [f for f in listdir(new_folder) if isfile(join(new_folder, f))]
#     print(*files, sep = "\n")
#
#     # Get name for processed file
#     regex = r"([^\/]+)(?=\-all)"
#     matches = re.search(regex, raw_submissions)
#     new_file = matches.group(1)
#
#     # Create list of columns to keep
#     keep_cols = ['id', 'created_utc', 'author', 'title',\
#                   'score', 'num_comments', 'subreddit', 'author_flair_text']
#
#     keep_cols_text = ['id', 'created_utc', 'author', 'selftext']
#
#     # Create file name
#     processedfile_csv = "data/processed/submissions/" + new_file + \
#         "-metadata" +  ".csv"
#
#     processed_textfile_csv = "data/processed/submissions/" + new_file + \
#         "-text" + ".csv"
#
#  # set up counter to determine whether to write or append to file
#
#     for i in files:
#         counter = 0
#
#         # Create empty data frame
#         df_keep = pd.DataFrame()
#         df_keep_text = pd.DataFrame()
#
#         # Set new file path based on folder name
#         file_path = new_folder + "/" + i
#
#
#         # Read in with chunk size arg
#         j_reader = pd.read_json(raw_submissions, lines = True, chunksize = 1000)
#
#         for i in j_reader:
#             counter += 1
#
#             # Keep only relevant columns
#             try:
#                 df_keep = i[keep_cols]
#
#             except KeyError:
#                 keep_cols = ['id', 'created_utc', 'author', 'title',\
#                             'score', 'num_comments', 'subreddit']
#                 df_keep = i[keep_cols]
#
#             try:
#                 df_text = i[keep_cols_text]
#             except KeyError:
#                 keep_cols_text = ['id', 'created_utc', 'author']
#                 df_text = i[keep_cols_text]
#
#             # Make sure there's at least 1 observation
#             observations = len(df_keep.index)
#
#             # If there are no observations, move to next subreddit
#             if observations == 0:
#                 print("No comments found in " + i)
#                 continue
#
#             # Change date format
#             ## For metadata
#             else:
#                 df_keep['datetime_dv'] = pd.to_datetime(df_keep['created_utc'], unit = 's')# dv = derived
#                 df_keep['date_dv'] = df_keep['datetime_dv'].dt.date
#
#                 # For text
#                 df_keep_text['datetime_dv'] = pd.to_datetime(df_keep_text['created_utc'], unit = 's')# dv = derived
#                 df_keep_text['date_dv'] = df_keep_text['datetime_dv'].dt.date
#
#             # Keep only observations within date limits
#             ##### Delimit by date #####
#             start = dt.datetime.fromtimestamp(utils.get_startdate()).date()
#             end = dt.datetime.fromtimestamp(utils.get_enddate()).date()
#
#             # Create mask of time slot
#             mask = (df_keep['date_dv'] >= start) & (df_keep['date_dv'] <= end) # inclusive on either end
#             mask_text = (df_keep_text['date_dv'] >= start) & (df_keep_text['date_dv'] <= end)
#
#             # Only keep data within date frame
#             df_keep = df_keep.loc[mask]
#             df_keep_text = df_keep_text.loc[mask_text]
#             ############################
#
#             ## Not formatting to date time now since can parse it when reading in the file
#
#
#             if counter == 1:
#                 df_keep.to_csv(processedfile_csv, mode = "w")
#                 df_keep_text.to_csv(processed_textfile_csv, mode = "w")
#
#             else:
#                 df_keep.to_csv(processedfile_csv, mode = "a", header = False)
#                 df_keep_text.to_csv(processed_textfile_csv, mode = "a", header = False)
#
#             del df_keep
#             del df_keep_text


#################
        # Read in all json files
        # try:
        #     data = pd.read_json(raw_submissions)
        #
        # # ValueError: Trailing data thrown if file is pretty indented
        # except ValueError:
        #     data = pd.read_json(raw_submissions, lines = True)
        #
        # try:
        #     df_keep = df_keep.append(data[keep_cols])
        # except KeyError:
        #     keep_cols = ['id', 'created_utc', 'author', 'title',\
        #                 'score', 'num_comments', 'subreddit'] # relevant submission columns
        #     df_keep = df_keep.append(data[keep_cols])
        #
        # try:
        #     df_keep_text = df_keep_text.append(data[keep_cols_text])
        # except KeyError:
        #     keep_cols_text = ['id', 'created_utc', 'author']
        #     df_keep_text = df_keep_text.append(data[keep_cols_text])
        #
        # # Make sure there's at least 1 observation
        # observations = len(df_keep.index)
        #
        # # If there are no observations, move to next subreddit
        # if observations == 0:
        #     print("No submissions found in " + i)
        #     continue
        #
        # # Else change date format
        # else:
        #     ## For metadata
        #     df_keep['datetime_dv'] = pd.to_datetime(df_keep['created_utc'], unit = 's')# dv = derived
        #     df_keep['date_dv'] = df_keep['datetime_dv'].dt.date
        #
        #     # For text
        #     df_keep_text['datetime_dv'] = pd.to_datetime(df_keep_text['created_utc'], unit = 's')# dv = derived
        #     df_keep_text['date_dv'] = df_keep_text['datetime_dv'].dt.date
        #
        #
        # ##### Delimit by date #####
        # start = dt.datetime.fromtimestamp(utils.get_startdate()).date()
        # end = dt.datetime.fromtimestamp(utils.get_enddate()).date()
        #
        # # Create mask of time slot
        # mask = (df_keep['date_dv'] >= start) & (df_keep['date_dv'] <= end) # inclusive on either end
        # mask_text = (df_keep_text['date_dv'] >= start) & (df_keep_text['date_dv'] <= end)
        #
        # # Only keep data within date frame
        # df_keep = df_keep.loc[mask]
        # df_keep_text = df_keep_text.loc[mask_text]
        # ############################
        #
        # # Save to csv
        # if counter == 1:
        #     df_keep.to_csv(processedfile_csv, mode = "w")
        #     df_keep_text.to_csv(processed_textfile_csv, mode = "w")
        #
        # else:
        #     df_keep.to_csv(processedfile_csv, mode = "a", header = False)
        #     df_keep_text.to_csv(processed_textfile_csv, mode = "a", header = False)
        #
        # del df_keep
        # del df_keep_text

if __name__ == "__main__":

    # Get comment folders
    comment_files = glob.glob("data/raw/comments/*.json")

    for i in comment_files:
        clean_comments(i)
        print(i + " cleaned")

    # Get submission files
    submissions_files = glob.glob("data/raw/submissions/*.json")

    for i in submissions_files:
        clean_submissions(i)
        print(i + " cleaned")
