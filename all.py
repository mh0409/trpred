# Load modules
import pandas as pd
import requests
import json
import csv
import time
import datetime as dt
from psaw import PushshiftAPI # https://github.com/dmarx/psaw

## Submissions
def crawl_page(subreddit: str, last_posttime = None):
    """Crawl a page of results from a given subreddit.
    :param subreddit: The subreddit to crawl.
    :param last_page: The last downloaded page.
    :return: A page of results.
    """

    url = "https://api.pushshift.io/reddit/search/submission"

    params = {"subreddit": subreddit,\
               "size": 500,\
               "sort": "desc",\
               "sort_type": "created_utc"}

    # Called to "scroll down" page based on before
    if last_posttime is not None:
        queries["before"] = last_posttime

    results = requests.get(url, params)

    if not results.ok:
        # something wrong happened
        raise Exception("Server returned status code {}".format(results.status_code))
    return results.json()["data"]


def crawl_subreddit(subreddit, max_submissions = 200000):
    """Crawl submissions from a subreddit.
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The maximum number of submissions to download.
    :return: A list of submissions."""

    all_submissions = [] # empty list to hold all submissions
    last_posttime = None  # will become an empty list when reached the last page

    while len(all_submissions) < max_submissions:
        current_submissions = get_pages(subreddit, last_posttime)
        if len(current_submissions) == 0:
            break
        last_posttime = current_submissions[-1]["created_utc"]
        all_submissions += current_submissions

        #time.sleep(3)

        if len(all_submissions) % 10000 == 0: # to track progress for big pulls
            print(len(all_submissions))
    return all_submissions[:max_submissions]

## Comments
def crawl_comments(subreddit, max_comments = 10000000):
    """Crawl comments from a subreddit
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The max number of comments to download.
    :return: a data frame of comments"""

    api = PushshiftAPI()

    gen = api.search_comments(subreddit = subreddit)

    comments = []

    for c in gen:
        comments.append(c)

        if len(comments) % 10000 == 0:
            print(len(comments))
         # Omit this to not limit to max_comments
#         if len(comments) >= max_comments:
#             break

    # Below code only used if the `if len(comments)` lines above not commented out
    if False: # False flag - to be changed to True if we want to get rest of the results
        for c in gen:
            comments.append(c)

    # Create pandas data frame to return
    df = pd.DataFrame([obj.d_ for obj in comments])

    return df
