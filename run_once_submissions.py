import all
import datetime as dt
import pandas as pd
import os
import json

### SUBMISSIONS ###

# Get number of submissions in entire subreddit
# requests.get(url, params = {"subreddit": "TheRedPill", "size": 0, "aggs" : "subreddit"}).json()["aggs"]
# Result (May 15th): 112,196 posts in the entire subreddit

# Get date
today = dt.datetime.utcnow().date()

## COMMENTED OUT BC ADDED ANCILLARY SUBREDDITS
# # Get r/TRP submissions
submissions = all.crawl_subreddit("TheRedPill")

# Save data as .json
os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing_Institute/trpred/data/raw/submissions") # change wd
filename = str("TheRedPill") + "-allsubmissions-" + str(today) + ".json" # create filename

with open(filename, 'w', encoding='utf-8') as f: # write file
    json.dump(submissions, f, ensure_ascii = False, indent=4)

# subreddits = ["RedPillWomen", "askTRP", "RedPillParenting", "thankTRP", "becomeaman", "altTRP", "GEOTRP", "TRPOffTopic"]

# for s in subreddits:
#     # Get submissions
#     submissions = all.crawl_subreddit(s)

#     # Save data as .json

#     os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing_Institute/trpred/data/raw/submissions") # change wd
#     filename = str(s) + "-submissions-asof-" + str(today) + ".json" # create filename

#     with open(filename, 'w', encoding='utf-8') as f: # write file
#         json.dump(submissions, f, ensure_ascii = False, indent=4)
