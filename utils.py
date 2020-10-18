# Load modules
import pandas as pd
import requests
import json
import os
import csv
import re
import time
import glob
import datetime as dt
from os import listdir
from os.path import isfile, join
from fsplit.filesplit import FileSplit
from psaw import PushshiftAPI # https://github.com/dmarx/psaw


def create_folder(raw_file, file_type):

    if file_type not in ["submissions", "comments"]:
        raise NameError("file_type must be either 'submissions' or 'comments'.")

    filename = get_filename(raw_file) # get the filename to create folder
    path = "data/raw/" + file_type + "/" + filename

    try:
        os.mkdir(path) # create directory

    except OSError:
        print("Creation of the directory %s failed" % path)

    else:
        print ("Successfully created the directory %s" % path)
        chunk_file(path)

    return path



def describe_file(f, s, c):
    print("file: {0}, size: {1}, count: {2}".format(f, s, c))


def chunk_file(folder_path):
        '''Split large files into 15MB chunks in identically-named folder.
        Assumes file and folder named identically. '''

        file_path = folder_path + ".json"

        dir = os.listdir(folder_path)

        # If folder is empty (i.e. file hasn't been split yet)...
        if len(dir) == 0:
            print("Folder is empty; raw file to be split")

            # ...then split file
            fs = FileSplit(file = file_path, splitsize = 15000000, output_dir = folder_path)

            fs.split(callback = describe_file)

def get_filename(file_path):
    regex = r"([^\/]+)(?=\.json$)" # set regex to get file names
    matches = re.search(regex, file_path)
    filename = matches.group()

    return filename

def get_startdate():
    start = int(dt.datetime(2012,10,25,0,0).timestamp())
    return start

def get_enddate():
    end = int(dt.datetime(2018,9,1,0,0).timestamp())
    return end

def get_subreddits():
    subreddits = []

    with open('data/reference/subreddits_of_interest.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                subreddits.append(row)

    # Subreddits hold the final list of subreddits we expect to have
    all_subreddits = list(set([x for x in subreddits[0]]))

    return all_subreddits

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

    #     reader = csv.reader(f,delimiter = ",")
    #     line_count = sum(1 for line in f)
    # return line_count - 1 # subtracting 1 bc of header

def count_processedentries(data_type):
    df_totals = pd.DataFrame(columns = ['subreddit', 'total'])

    if data_type == "comments":
        files = glob.glob("data/processed/comments/*-metadata.csv")


    if data_type == "submissions":
        files = glob.glob("data/processed/submissions/*-metadata.csv")

    else:
        raise ValueError("Invalid data_type: must be either \
        'comment' or 'submission'")

    for i in files:
        # get name of subreddit from file name
        regex = r"^.*\/([^-]*)-.*$"
        matches = re.search(regex, i)
        subreddit = matches.group(1)

        # get the length of the file using helper function
        total = file_len(i)

        df_totals = df_totals.append({'subreddit':subreddit, 'total':total}, ignore_index = True)

    return df_totals
