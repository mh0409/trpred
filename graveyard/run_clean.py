#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:45:00 2020

@author: mariajoseherrera
"""
from glob import glob
import clean
import re

# Load file names


### r/TheRedPill only
## Submissions
# trp_subdaily = glob(("data/raw/submissions/*-dailysubmissions-*.json")) # daily scrapes
# trp_suball = glob("data/raw/submissions/*-allsubmissions-*.json") # the big scrape
# trp_submissions = trp_suball + trp_subdaily

## TODO: Bring glob into clean.py file? so that you only have to specify subreddit when cleaning?

## Comments
# trp_comdaily = glob(("data/raw/comments/daily*.json")) # daily scrapes # TODO: FIX THESE JSON FILES -- THEYRE MESSSED UP
#trp_comall = glob("data/raw/comments/all_TRP/*.json") # the big scrape

#trp_comments =  trp_comall # + trp_comdaily  # COMMENTED OUT BC DAILY FILES ARE BROKEN

## Clean submission data
# sub_cols = clean.clean_subreddit(trp_submissions, "TheRedPill",\
#   "submissions")
# print(sub_cols)

# # Clean comment data
# com_cols = clean.clean_subreddit(trp_comments, "TheRedPill","comments")
# print(com_cols)
###

### Ancillary subreddits
# ## TODO: set up individual subreddit folders in raw file / so can just scrape into those files directly and only have to read stuff once
# ancillary_submissions = glob("data/raw/submissions/ancillary/*.json") # the big scrape
#
#
# # Clean submission data
# ancillary_sub_cols = clean.clean_subreddit(ancillary_submissions, "AllAncillary",\
#   "submissions")
# print(ancillary_sub_cols)
#
# # Get comment data
# ancillary_comall = glob("data/raw/comments/ancillary/*.json") # the big scrape
#
#
# # Clean comment data
# ancillary_com_cols = clean.clean_subreddit(ancillary_comall, "AllAncillary", "comments")
# print(ancillary_com_cols)
