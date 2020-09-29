import pandas as pd
import re
import datetime as dt
import csv
import os
from os import listdir
from os.path import isfile, join
from fsplit.filesplit import FileSplit
import clean


os.chdir("/Volumes/SAMSUNG/trpred")

##### SECTION COMMENTED OUT BC ONLY NEED TO DO ONCE
#
# # Create subdirectory for each subreddit
#
## Step 1: Get names for new folders
# from glob import glob
# comment_files = glob("data/raw/comments/*.json")
#
# 
# regex = r"([^\/]+)(?=\.json$)"
#
# filenames = []
#
# for i in comment_files:
#     matches = re.search(regex, i)
#     new_file = matches.group()
#     filenames.append(new_file)
#
# ## Step 2: Create directories with file names
#
# # define the name of the directory to be created
# for i in filenames:
#     path = "data/raw/comments/" + i
#
#     try:
#         os.mkdir(path)
#     except OSError:
#         print ("Creation of the directory %s failed" % path)
#     else:
#         print ("Successfully created the directory %s" % path)
# #
# #
# # Function will tell you file name, size in bytes, and line count
# def func(f, s, c):
#     print("file: {0}, size: {1}, count: {2}".format(f, s, c))
#
# ## Step 3: Split files into corresponding folder
# for i in filenames:
#     file_path = "data/raw/comments/" + i + ".json"
#     folder_path = "data/raw/comments/" + i + "/"
#
#     dir = os.listdir(folder_path)
#
#     print(dir)
#
#     # If folder is empty (i.e. file hasn't been split yet)...
#     if len(dir) == 0:
#         print("folder is empty")
#
#         # ...then split file
#         fs = FileSplit(file = file_path, splitsize = 15000000, output_dir = folder_path)
#
#         fs.split(callback = func)
#
# #############

# Now clean every small file for all subreddit folders

# Get folder names
# subreddit_folders = [x[0] for x in os.walk("data/raw/comments")]
# subreddit_folders = subreddit_folders[1:] # item at index 0 is parent folder so exclude
#
subreddit_folders = ["data/raw/comments/TumblrInAction-allcomments-2020-09-27"]

for i in subreddit_folders:
    # Pass in folder name to method
    clean.clean_comments(i)
    print(i + " complete")
