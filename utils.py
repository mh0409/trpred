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
    regex = r"([^\/]+)(?=\.$)" # set regex to get file names
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

def count_processedentries(data_type):
    df_totals = pd.DataFrame(columns = ['subreddit', 'total'])

    if data_type == "comments":
        files = glob.glob("data/processed/comments/*-metadata.csv")


    elif data_type == "submissions":
        files = glob.glob("data/processed/submissions/*-metadata.csv")

    else:
        raise ValueError("Invalid data_type: must be either 'comments' or 'submissions'")

    for i in files:
        # get name of subreddit from file name
        regex = r"^.*\/([^-]*)-.*$"
        matches = re.search(regex, i)
        subreddit = matches.group(1)

        # get the length of the file using helper function
        total = file_len(i)

        df_totals = df_totals.append({'subreddit':subreddit, 'total':total}, ignore_index = True)

    return df_totals

def dedupe(filename):
    df_dupe = pd.read_csv(filename)
    df_new = df_dupe.drop_duplicates(subset = ['id'])
    df_new.to_csv(filename, index=False)

def get_submissions_aggs(subreddit_names):

    # Get count of submissions per subreddit above
    subred_posts = {}

    start = utils.get_startdate()
    end = utils.get_enddate()

    # Get number of comments of all time (sanity check)
    for s in subreddit_names:
        url = "https://api.pushshift.io/reddit/search/submission/"
        queries = {"subreddit": s,\
                    "size": 0,\
                    "aggs" : "subreddit",\
                    "after": start,\
                    "before": end}

        r = requests.get(url, params = queries)

        # Get count (sanity check)
        try:
            count_posts = r.json()["aggs"]["subreddit"][0]["doc_count"]
        except:
            count_posts = np.nan

        subred_posts[s] = count_posts

    df_subred_posts = pd.DataFrame.from_dict(subred_posts, orient = "index", columns = ["posts"])
    df_subred_posts.index.name = 'subreddit'
    df_subred_posts.reset_index(inplace=True)

    file_name = "data/info/"+dt.datetime.today.strftime('%Y%m%d')+"_post_counts_by_subreddit.csv"
    df_subred_posts.to_csv(file_name)

    return df_subred_posts

def get_comments_aggs(subreddit_names):

    start = str(utils.get_startdate())
    end = str(utils.get_enddate())

    # Get count of comments per subreddit above
    subred_comments = {}

    # Get number of comments in all time (sanity check)
    for s in subreddit_names:
        url = "https://api.pushshift.io/reddit/search/comment/"
        queries = {"subreddit": s,\
                    "size": 0,\
                    "aggs" : "subreddit",\
                    "after": start,\
                    "before": end}

        r = requests.get(url, params = queries)


        # Get count (sanity check)
        try:
            count_comments = r.json()["aggs"]["subreddit"][0]["doc_count"]
        except:
            count_comments = np.nan

        subred_comments[s] = count_comments

        df_subred_comments = pd.DataFrame.from_dict(subred_comments, orient = "index", columns = ["comments"])
        df_subred_comments.index.name = 'subreddit'
        df_subred_comments.reset_index(inplace=True)

        file_name = "data/info/"+dt.datetime.today.strftime('%Y%m%d')+"_comment_counts_by_subreddit.csv"
        df_subred_comments.to_csv("data/info/20201004_commentcounts_by_subreddit.csv")

    return df_subred_comments

def get_subreddit_from_filename(file_path):
    # get name of subreddit from file name
    regex = r"^.*\/([^-]*)-.*$"
    matches = re.search(regex, file_path)
    subreddit = matches.group(1)
    return subreddit

def get_authors(file_type):
    # Load in one example
    file_ls = glob("data/processed/metadata/" + str(file_type) "/*metadata.csv")
    file_ls = list(dict.fromkeys(file_ls))

    df_all_authors = pd.DataFrame(columns=['author', 'subreddit', 'num_items'])

    df_all_unique_users  = pd.DataFrame(columns=['subreddit', 'num_unique_users'])


    for i in file_ls:
        # Load in file; only interested in author and subreddit columns
        df_items = pd.read_csv(i, usecols=['author', 'subreddit'])

        # get name of subreddit from file name
        subreddit = get_subreddit_from_filename(i)

        ## per subreddit
        authors_items = df_items.author.unique()

        # get number of posts
        counts = df_items.author.value_counts()

        df_authors = pd.DataFrame({'author': authors_items})
        df_authors['subreddit'] = subreddit
        df_authors = pd.merge(df_authors, counts, how = 'left', left_on = 'author', right_index = True)

        df_authors.columns = ['author', 'subreddit', 'num_items']

        df_all_authors = pd.concat([df_all_authors, df_authors])

        return df_all_authors


def get_unique_users(file_type):

    # Load in files
    file_ls = glob("data/processed/metadata/" + str(file_type) "/*metadata.csv")
    file_ls = list(dict.fromkeys(file_ls))

    for i in file_ls:
        # Load in file; only interested in author and subreddit columns
        df_items = pd.read_csv(i, usecols=['author', 'subreddit'])

        # get name of subreddit from file name
        subreddit = get_subreddit_from_filename(i)

        ## per subreddit
        authors_items = df_items.author.unique()

        # Get number unique users
        ## per subreddit
        unique_users = len(authors_items)

        df_users = pd.DataFrame({'subreddit': [subreddit]})
        df_users['num_unique_users'] = unique_users

        df_all_unique_users = pd.concat([df_all_unique_users, df_users])

    return df_all_unique_users

def get_descriptions():
    ''' Saves down descriptions '''
    all_subreddits = utils.get_subreddits()

    # Get descriptions of subreddit
    subred_descriptions = {}

    for i in all_subreddits:
        subreddit = reddit.subreddit(i) # create instance of subreddit

        try:
            description = subreddit.public_description # get attribute
        except:
            description = "NA - either banned or quarantined"

        if description == "":
            description = "NA - no description listed"

        subred_descriptions[i] = description

    # For more info on subreddit instances / possible attributes on PRAW:
    # https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html


    # Create a data frame based on subreddits and descriptions
    df_descriptions = pd.DataFrame.from_dict(subred_descriptions, orient = "index", columns = ["public_description"])
    df_descriptions = df_descriptions.reset_index()
    df_descriptions = df_descriptions.rename(columns = {"index":"subreddit"})

    # Save to file
    today = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d")
    df_descriptions.to_csv("data/info/"+today+"_subreddit_descriptions.csv")


def get_trp_flair():
    file_ls = ["data/processed/comments/TheRedPill-metadata.csv", "data/processed/submissions/TheRedPill-allsubmissions-2020-05-16-metadata.csv"]

    for i in file_ls:
        # Get all trp users from submissions
        users_submissions = pd.read_csv(file_path, usecols = ["id","author"])

        # Get submission ids to search for author flair by submission
        ls_subids = list(users_submissions.id)

        counter = 0

        today = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d")

        if "submissions" in file_path:
            type = "submissions"

        else:
            type = "comments"

        filename = "data/info/" + today + "_" + type + "_trp_user_flairs.json"

        # initializing empty dict
        trpuser_flairs = {}

        for i in ls_subids:
            # set url to search by submission id
            url = "https://api.pushshift.io/reddit/submission/search/?ids="
            url = url + i # concat id from list
            r = requests.get(url) # make request

            author = users_submissions.loc[users_submissions['id'] == i]['author']
            author = author.values[0]

            try:
                flair = r.json()['data'][0]['author_flair_text'] # get flair if it exists
            except:
                flair = np.nan # otherwise, no flair

            trpuser_flairs[author] = flair

            print(i)
            counter += 1
            print("og start +:", counter)

            time.sleep(1)

            if len(trpuser_flairs.keys()) % 1000 == 0:
                try:
                    with open(filename, 'wb') as outfile:
                        json.dump(trpuser_flairs, outfile)
                except:
                    continue
