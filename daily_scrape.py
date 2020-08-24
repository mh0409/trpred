# Load modules
import pandas as pd
import requests
import json
import csv
import time
import datetime as dt
from psaw import PushshiftAPI # https://github.com/dmarx/psaw

## Submissions code
def get_pages(subreddit: str, last_posttime = None):
    """Crawl a page of results from a given subreddit over the past day.
    :param subreddit: The subreddit to crawl.
    :param last_posttime: The last downloaded page.
    :return: A page of results.
    """
    url = "https://api.pushshift.io/reddit/search/submission"

    # Calculate time window for past day
    today = dt.datetime.utcnow().date()
    yesterday = today - dt.timedelta(days = 1) # will count/collect posts after 00:00 on this date

    queries = {"subreddit": subreddit,\
               "size": 500,\
               "sort": "desc",\
               "sort_type": "created_utc",\
               "before": today,\
               "after": yesterday}

    # Called to "scroll down" page based on before
    if last_posttime is not None:
        queries["before"] = last_posttime

    # Request data
    results = requests.get(url, params = queries)

    # Check for errors
    if not results.ok:
        # something wrong happened
        raise Exception("Server returned status code {}".format(results.status_code))

    return results.json()["data"]


def get_dailysubmissions(subreddit, max_submissions = 200000):
    """Crawl submissions from a subreddit over past day (hard coded in `get_pages()`).
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The maximum number of submissions to download.
    :return: A list of submissions."""

    # Calculate time window
    today = dt.datetime.utcnow().date()
    yesterday = today - dt.timedelta(days = 1) # will count/collect posts after 00:00 on this date

    all_submissions = [] # empty list to hold all submissions
    last_posttime = None # will become an empty list when reached the last page


    while len(all_submissions) < max_submissions:
        current_submissions = get_pages(subreddit, last_posttime)
        if len(current_submissions) == 0:
            break
        last_posttime = current_submissions[-1]["created_utc"]
        all_submissions += current_submissions
        time.sleep(45)
        if len(all_submissions) % 100 == 0: # to track progress for pulls
            print(len(all_submissions))

    # Print final length of submissions
    print(len(all_submissions))

    # Save comments
    filename_json = "data/raw/submissions/" + str(subreddit) + "-dailysubmissions-" + str(yesterday) + ".json" # create filename

    for obj in all_submissions:
        with open(filename_json, 'a', encoding = 'utf-8') as fp:
            json.dump(obj, fp, ensure_ascii = False) # write file
            fp.write('\n')

    return # empty return -- file saved


## Comments code
def get_dailycomments(subreddit, before, after, max_comments = 10000000):
    """Get comments from a subreddit over the past day
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The max number of comments to download.
    :return: a data frame of comments"""

    # Calculate time window
    today = dt.datetime.utcnow().date()
    yesterday = today - dt.timedelta(days = 1) # will count/collect posts after 00:00 on this date

    # Create instance of API
    api = PushshiftAPI()

    # Using psaw package to access comments
    gen = api.search_comments(subreddit = subreddit,\
                              before = before,\
                             after = after)

    # Create empty container for comments
    comments = []

    for c in gen:
        comments.append(c) # append each item in generator



        if len(comments) % 100 == 0: # track progress for large pulls
            print(len(comments))

        # Omit this to not limit to max_comments
       # if len(comments) >= max_comments:
       #      break



    # Below code only used if the `if len(comments)` lines above not commented out
    # if False: # False flag - to be changed to True if we want to get rest of the results
    #     for c in gen:
    #         comments.append(c)

    # Print final length of comments
    print(len(comments))

    # Save comments
    filename_json = "data/raw/comments/" + str(subreddit) + "dailycomments-" + str(yesterday) + ".json" # create filename

    # // TODO: create json readr/writr function

    for obj in comments:
        with open(filename_json, 'a', encoding = 'utf-8') as fp:
            json.dump(obj.d_, fp, ensure_ascii = False) # write file
            fp.write('\n')

    return # empty return -- file saved
