import os
import csv
import pandas as pd
import utils
import datetime as dt

def get_descriptions(subreddits):
    ls_subreddits = []

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

if __name__ == "__main__"
    # Load list of subreddits of interest
    ls_subreddits = utils.get_subreddits()

    get_descriptions(ls_subreddits)
