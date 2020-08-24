import all_scrape as all
import datetime as dt
import pandas as pd
import os
import json
import time

### SUBMISSIONS ###

# Get number of submissions in entire subreddit
# requests.get(url, params = {"subreddit": "TheRedPill", "size": 0, "aggs" : "subreddit"}).json()["aggs"]
# Result (May 15th): 112,196 posts in the entire subreddit

# Get date
today = dt.datetime.utcnow().date()

## COMMENTED OUT BC ADDED ANCILLARY SUBREDDITS

##### JUST R/TRP ########
# # Get r/TRP submissions
# submissions = all.crawl_subreddit("TheRedPill")
#
# # Save data as .json
# os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing_Institute/trpred/data/raw/submissions") # change wd
# filename = str("TheRedPill") + "-allsubmissions-" + str(today) + ".json" # create filename
#
# with open(filename, 'w', encoding='utf-8') as f: # write file
#     json.dump(submissions, f, ensure_ascii = False, indent=4)
#########################


subreddits = [#"RedPillWomen",\
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
             #  "Egalitarianism", "exredpill", \
              # "FeMRADebates",\
              # "GEOTRP", "IncelsInAction", "IncelsWithoutHate",\
              # "masculism", "MensRants", \
              # "MensRights",\
              # "mensrightslaw",\
              # "MensRightsMeta",\
              # "MGTOW",\
              # "mgtowbooks","MRActivism",\
              # "NOMAAM", "pua",
              # "PurplePillDebate",\
              # "seduction",\
               # "Trufemcels"\
               ]

for s in subreddits:
    # Get submissions
    all.crawl_subreddit(s)
    print(s+" done")
    time.sleep(3)

    # Save data as .json
    ## ALREADY DOING THIS IN THE ALL_SRAPE.PY FILE SO DELETE BELOW?
    # os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing_Institute/trpred/data/raw/submissions") # change wd
    # filename = str(s) + "-submissions-asof-" + str(today) + ".json" # create filename
    #
    # with open(filename, 'w', encoding='utf-8') as f: # write file
    #     json.dump(submissions, f, ensure_ascii = False, indent=4)
