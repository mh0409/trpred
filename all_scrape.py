# Load modules
import pandas as pd
import requests
import json
import csv
import time
import datetime as dt
from psaw import PushshiftAPI # https://github.com/dmarx/psaw

## Submissions
def get_pages(subreddit: str, last_posttime = None):
    """Crawl a page of results from a given subreddit.
    :param subreddit: The subreddit to crawl.
    :param last_page: The last downloaded page.
    :return: A page of results.
    """

    url = "https://api.pushshift.io/reddit/search/submission"

    queries = {"subreddit": subreddit,\
               "size": 500,\
               "sort": "desc",\
               "sort_type": "created_utc"}

    # Called to "scroll down" page based on before
    if last_posttime is not None:
        queries["before"] = last_posttime

    results = requests.get(url, queries)

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
    today = dt.datetime.utcnow().date()

    filename = "data/raw/submissions/" + str(subreddit) + "-allsubmissions-" + str(today) + ".json" # create filename

    k = 0 # get accurate number of posts in a subreddit

    while len(all_submissions) < max_submissions:
        current_submissions = get_pages(subreddit, last_posttime)
        if len(current_submissions) == 0:
            break
        last_posttime = current_submissions[-1]["created_utc"]
        all_submissions += current_submissions

        time.sleep(3)

        counter = len(all_submissions)

        if counter % 1000 == 0: # to track progress for big pulls
            k += 1
            print(counter*k) # number of posts that have been recorded

            for obj in all_submissions:
                with open(filename, 'a', encoding='utf-8') as f: # write file
                    json.dump(obj, f, ensure_ascii = False)
                    f.write('\n')

            all_submissions = []

    for obj in all_submissions:
        with open(filename, 'a', encoding='utf-8') as f: # write file
            json.dump(obj, f, ensure_ascii = False)
            f.write('\n')


    return # empty return - saved file

## Comments
def crawl_comments(subreddit, before = None, after = None, max_comments = None):
    """Crawl comments from a subreddit
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The max number of comments to download.
    :return: empty - saved file"""

    api = PushshiftAPI()

    if before is None and after is None:
        gen = api.search_comments(subreddit = subreddit)
    else:
        gen = api.search_comments(subreddit = subreddit,
                                 before = before,
                                 after = after)

    comments = []
    doc_num = []
    today = dt.datetime.utcnow().date()
    filename_json = "data/raw/comments/" + str(subreddit) + "-allcomments-" + str(today) + ".json"
    counter = 0

    for c in gen:
        comments.append(c)
        counter += 1

        if counter % 10000 == 0:
            # Incrementally save and append json
            for obj in comments:
                with open(filename_json, 'a', encoding = 'utf-8') as fp:
                    json.dump(obj.d_, fp, ensure_ascii = False) # write file
                    fp.write('\n')

            print(counter)

            comments = [] # empty comments container to avoid memory issues

         # Omit this to not limit to max_comments
        if max_comments is not None:
            if counter >= max_comments:
                 break

    # Final number of comments
    print(counter)

    # Save last batch of comments
    for obj in comments:
        with open(filename_json, 'a', encoding = 'utf-8') as fp:
            json.dump(obj.d_, fp, ensure_ascii = False) # write file
            fp.write('\n')




    # Below code only used if the `if len(comments)` lines above not commented out
    #if False: # False flag - to be changed to True if we want to get rest of the results
    #    for c in gen:
    #        comments.append(c)



    return # empty return, saved file
