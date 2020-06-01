import os
import daily
import datetime as dt
import json
import pandas as pd

# Get Submissions
daily.get_dailysubmissions("TheRedPill")


# Pull past day's comments
# Calculate time window
today = dt.datetime.utcnow().date()
yesterday = today - dt.timedelta(days = 1) # will count/collect posts after 00:00 on this date


daily.get_dailycomments("TheRedPill", today, yesterday)
