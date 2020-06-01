import all
import datetime as dt
import pandas as pd
import os
import json
from dateutil.relativedelta import relativedelta


## Comments

# Get past two years
# today = dt.datetime.utcnow().date()
# two_yrs_ago = today - relativedelta(years = 2)
#
# all.crawl_comments("TheRedPill", before = today, after = two_yrs_ago)

# Get all comments
all.crawl_comments('TheRedPill')


# Get comments for ancillary subreddits
# subreddits = ["RedPillWomen", "askTRP", "RedPillParenting", "thankTRP", "becomeaman", "altTRP", "GEOTRP", "TRPOffTopic"]

# for s in subreddits:
#      all.crawl_comments(s)
