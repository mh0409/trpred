import utils
import datetime as dt
import pandas as pd
import os
import time
import json
from dateutil.relativedelta import relativedelta
# Load modules
import pandas as pd
import requests
import json
import csv
import re
import time
import datetime as dt
from psaw import PushshiftAPI # https://github.com/dmarx/psaw

latest_end = None

def get_latest_end():
    return latest_end

def set_latest_end(new_end):
    latest_end = new_end
    return latest_end

# Submissions
def get_pages(subreddit: str, range_start = None, range_end = None, last_posttime = None):
    """Crawl a page of results from a given subreddit.
    :param subreddit: The subreddit to crawl.
    :param last_page: The last downloaded page.
    :return: A page of results.
    """

    url = "https://api.pushshift.io/reddit/search/submission"

    queries = {"subreddit": subreddit,\
               "size": "100",\
               "sort": "desc",\
               "sort_type": "created_utc",
               "after": str(range_start),
               "before": str(range_end)}

    # Called to "scroll down" page based on before
    if last_posttime is not None:
        queries["before"] = str(last_posttime)

    print(queries)
    global latest_end
    latest_end = queries["before"]
    print("latest_end: ", latest_end)

    results = requests.get(url, queries)

    print(results)

    if not results.ok:
        # something wrong happened
        raise Exception("Server returned status code {}".format(results.status_code))
    return results.json()["data"]


def get_submissions(subreddit, after, before, max_submissions = 200000000):
    """Crawl submissions from a subreddit.
    :param subreddit: The subreddit to crawl.
    :param max_submissions: The maximum number of submissions to download.
    :return: A list of submissions."""

    print("inside get_submissions")

    all_submissions = [] # empty list to hold all submissions
    last_posttime = None  # will become an empty list when reached the last page
    earliest_posttime = None # same as above
    today = dt.datetime.utcnow().date()

    filename = "data/raw/submissions/" + str(subreddit) + "-allsubmissions-" + str(today) + ".json" # create filename

    k = 0 # get accurate number of posts in a subreddit

    # Define last and earliest last_posttime
    last_posttime = None

    while len(all_submissions) < max_submissions:
        print("about to call get pages")
        current_submissions = get_pages(subreddit, range_start = after, range_end = before, last_posttime = last_posttime)
        print("global latest_end: ", get_latest_end())
        if len(current_submissions) == 0:
            break
        last_posttime = current_submissions[-1]["created_utc"]
        all_submissions += current_submissions

        time.sleep(5)

        counter = len(all_submissions)
        print("counter: " + str(counter))

        if counter % 100 == 0: # to track progress for big pulls
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


    latest_end = before

    return # empty return - saved file


## Comments
def get_comments(subreddit, before = None, after = None, max_comments = None):
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
                                 after = after,
                                 size = 500)



    comments = []
    doc_num = []
    today = dt.datetime.utcnow().date()
    filename_json = "data/raw/comments/" + str(subreddit) + "-allcomments-" + str(today) + ".json"
    counter = 0

    for c in gen:
        print("counter: " + str(counter))
        comments.append(c)
        counter += 1

        if counter % 1000 == 0:
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

if __name__ == "__main__":
    # Load list of subreddits of interest
    ls_subreddits = utils.get_subreddits()

    # Get dates of dates of interest
    start = utils.get_startdate()
    end = utils.get_enddate()

    # Get submissions and comments:
    for i in ls_subreddits:
        utils.crawl_submissions(i, after = start, before = end)
        print(s+" submissions collected")

        utils.crawl_comments(i, after = start, before = end)
        print(s+" comments collected")
