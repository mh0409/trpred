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


def create_folder(raw_comments):
    filename = get_filename(raw_comments) # get the filename to create folder

    path = "data/raw/comments/" + filename

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

        print(dir)

        # If folder is empty (i.e. file hasn't been split yet)...
        if len(dir) == 0:
            print("folder is empty")

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
    with open('~/data/reference/subreddits_of_interest.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
                subreddits.append(row)

    # Subreddits hold the final list of subreddits we expect to have
    all_subreddits = list(set([x for x in subreddits[0]]))

    return all_subreddits
