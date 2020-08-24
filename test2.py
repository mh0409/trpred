from glob import glob
import clean
import pandas as pd
import datetime as dt
import csv

comments = glob("data/raw/comments/*.json")

for i in comments[20:]: # start at 18 to get the other one
    # print(i)
    clean.clean_subreddit(i,"comments")
