import requests
import datetime as dt
import pandas as pd
import numpy as np
import utils

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

    start = utils.get_startdate()
    end = utils.get_enddate()

    # Get count of comments per subreddit above
    subred_comments = {}

    # Get number of comments in all time (sanity check)
    for s in all_subred:
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
