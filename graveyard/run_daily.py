import os
import daily_scrape as daily
import datetime as dt
import json
import pandas as pd
import clean as clean
import time
import glob

# Define ancillary subreddits
subreddits = [\
             #    "RedPillWomen",\
             #    "askTRP",\
             #    "RedPillParenting",\
             #    "thankTRP",\
             #    "RedPillLit",\
             #    "becomeaman",\
             #    "altTRP",\
             #    "GEOTRP",\
             #    "TRPOffTopic",\
             #     "u_TRP_Scepter",\
             #     "RedPillNonMonogamy",\
             #     "RedPillWives",\
             #     "redpillfatherhood",\
             #     "redpillbooks",\
             #     "RedPillWorkplace",\
             #     "theRedPillLeft",\
             #     "TRPmemes",\
             #     "theredpillright",\
             #     "EthnicRedPill",\
             #     "marriedredpill",\
             # "AskFeminists", "askseddit", "badwomensanatomy",\
             #  "Egalitarianism", "exredpill",\
               "FeMRADebates",\
              "GEOTRP", "IncelsInAction", "IncelsWithoutHate",\
              "masculism", "MensRants", "MensRights", "mensrightslaw",\
              "MensRightsMeta", "MGTOW", "mgtowbooks","MRActivism",\
              "NOMAAM", "pua", "PurplePillDebate", "seduction", "Trufemcels"]

# Get r/theredpill Submissions
daily.get_dailysubmissions("TheRedPill")

# Get ancillary submissions
for s in subreddits:
    daily.get_dailysubmissions(s)
    time.sleep(3) # to avoid 429 (rate limit) errors

# TODO: Figure out how to structure raw data folder to make cleaning easier
# TODO: decide whether to save all ancillary to one file or to separate by subreddit
# # Clean and save
# ancillary_submissions = glob("data/raw/submissions/ancillary/*.json") # the big scrape
#
#
# # Clean submission data
# ancillary_sub_cols = clean.clean_subreddit(ancillary_submissions, "AllAncillary",\
#   "submissions")
# print(ancillary_sub_cols)




# Pull past day's comments
# Calculate time window
today = dt.datetime.utcnow().date()
yesterday = today - dt.timedelta(days = 1) # will count/collect posts after 00:00 on this date

# Get r/TheRedPill comments
daily.get_dailycomments("TheRedPill", today, yesterday)

# Get ancillary Comments
for s in subreddits:
    daily.get_dailycomments(s, today, yesterday)
    # TODO: add command to move file to ancillary folder here?
    time.sleep(3)


# # Get comment data
# ancillary_comall = glob("data/raw/comments/ancillary/*.json") # the big scrape
#
#
# # Clean comment data
# ancillary_com_cols = clean.clean_subreddit(ancillary_comall, "AllAncillary", "comments")
# print(ancillary_com_cols)
