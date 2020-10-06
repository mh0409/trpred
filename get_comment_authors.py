import numpy as np
import os
import pandas as pd
import json
import csv
import time
import datetime as dt
from glob import glob
import requests
import re


# Change wd
os.chdir("/Volumes/SAMSUNG/trpred")

# Load in one example
file_subs = glob("data/processed/comments/*metadata.csv")
file_subs = list(dict.fromkeys(file_subs))

df_all_authors = pd.DataFrame(columns=['author', 'subreddit', 'num_posts'])

df_all_unique_users  = pd.DataFrame(columns=['subreddit', 'num_unique_users'])


for i in file_subs:

    df_subs = pd.read_csv(i, usecols=['author', 'subreddit'])

    # get name of subreddit from file name
    regex = r"^.*\/([^-]*)-.*$"
    matches = re.search(regex, i)
    subreddit = matches.group(1)

    ## per subreddit
    authors_submissions = df_subs.author.unique()

    # get number of posts
    counts = df_subs.author.value_counts()

    df_authors = pd.DataFrame({'author': authors_submissions})
    df_authors['subreddit'] = subreddit
    df_authors = pd.merge(df_authors, counts, how = 'left', left_on = 'author', right_index = True)

    df_authors.columns = ['author', 'subreddit', 'num_posts']

    df_all_authors = pd.concat([df_all_authors, df_authors])

    # Get number unique users
    ## per subreddit
    unique_users = len(authors_submissions)

    df_users = pd.DataFrame({'subreddit': [subreddit]})
    df_users['num_unique_users'] = unique_users

    df_all_unique_users = pd.concat([df_all_unique_users, df_users])

df_all_authors.to_csv("data/info/comments_all_authors.csv")
df_all_unique_users.to_csv("data/info/comments_num_users.csv")
