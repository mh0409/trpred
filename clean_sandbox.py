# Load modules
import os
import pandas as pd
import requests
import json
import csv
import time
from dateutil.relativedelta import relativedelta
import datetime as dt
from psaw import PushshiftAPI # https://github.com/dmarx/psaw
from glob import glob


# Load data


## Submissions

###### "KEEP ONLY DATA OF INTEREST" CODE BELOW ######

# Full subreddit scrape
df_allsubmissions = pd.read_json("data/raw/submissions/allsubmissions-2020-05-16.json") ## Only need to do once
## can't do the above with the daily files bc get "trailing data" error

# Create list of columns to keep ## HAVE TO BE CAREFUL HERE SINCE NOT ALL FILES HAVE ALL COLUMNS
keep_cols = ['author','id', 'title','created_utc',\
             'selftext', 'score', 'num_comments', 'subreddit']

df_keep = df_allsubmissions[keep_cols]

# Daily submissions
filenames = glob('data/raw/submissions/dailysubmissions*.json')

for file in filenames:
    
    # Read in json file
    try:
        data = pd.read_json(file)
        
    # ValueError: Trailing data error thrown if file is pretty indented
    except ValueError:
        data = pd.read_json(file, lines = True)
    
    df_keep.append(data[keep_cols])
    
    
    # with open(file) as f:
         
    #     data = []
          
    #     # Load in data for each file at a time
    #     for line in f:
    #         json_obj = json.loads(line)
    #         data.append(json_obj)
    #         break
       
    #     # 
    #     df = pd.DataFrame.from_dict(data)
     
    #     df_keep.append(df[keep_cols])

# Name aggregate file
today = dt.datetime.utcnow().date()
processedfile_csv = "data/processed/submissions/submissions-" + str(today) + ".csv"

# Save to json
df_keep.to_csv(processedfile_csv)
    

    
            