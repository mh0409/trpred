#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:43:47 2020

@author: mariajoseherrera
"""

import pandas as pd
import datetime as dt
import csv


def clean_subreddit(filenames, subreddit, data_type):
    """Cleans the list of files passed in as the first argument based on data type.
    Data_type takes values "submmissions" or "comments", else throws ValueError; 
    this determines the columns to be kept in the corresponding data frame. Saves 
    files to processed/submissions folder within trpred. Returns the column 
    headers we can expect to see in the saved file."""
    
    ## MAYBE REPLACE FILENAMES WITH SUBREDDIT AND MOVE GLOB INTO HERE
    ## or split into clean comments and clean submissions since comments are so much bigger
    
    
    # Get date for filename
    today = dt.datetime.utcnow().date()
    

    if data_type == "submissions": 
        # Create list of columns to keep 
        keep_cols = ['author','id', 'title','created_utc',\
                      'score', 'num_comments', 'subreddit']
        keep_cols_text = ['id', 'title','selftext']
            
        # Create file name
        processedfile_csv = "data/processed/submissions/"+ str(subreddit) +\
            "-submissions-"+ str(today) + ".csv"
            
        processed_textfile_csv = "data/processed/submissions/" + str(subreddit) +\
            "-submissionstext-" + str(today) + ".csv"

    elif data_type == "comments":
        # Create list of columns to keep
        keep_cols = ['id', 'author', 'created_utc',\
                      'author_flair_text', 'score', 'parent_id',\
                      'subreddit']
        keep_cols_text = ['id',  'parent_id', 'body']
        
        # Create file name
        processedfile_csv = "data/processed/comments/" + str(subreddit) +\
            "-comments-" + str(today) + ".csv"
 
        processed_textfile_csv = "data/processed/comments/" + str(subreddit) +\
            "-commentstext-" + str(today) + ".csv"
            
    else:
        raise ValueError("Unsupported data_type. 'data_type' only takes values\
                          'submissions' or 'comments'")
    
    df_keep = pd.DataFrame()
    df_keep_text = pd.DataFrame()
    
    for file in filenames:
        
        # Read in json file
        try:
            data = pd.read_json(file)
            
            
        # ValueError: Trailing data thrown if file is pretty indented
        except ValueError:
            data = pd.read_json(file, lines = True)
        
        df_keep = df_keep.append(data[keep_cols])   
        df_keep_text = df_keep_text.append(data[keep_cols_text])
        
        # Save to json
        df_keep.to_csv(processedfile_csv, mode = "a")    
        df_keep_text.to_csv(processed_textfile_csv, mode = "a")
        print(len(df_keep.index))
    
        
        data = [] # force empty   

    
    return keep_cols


with open(processedfile_csv, 'a', encoding = 'utf-8') as fp:
        json.dump(obj.d_, fp, ensure_ascii = False) # write file
        fp.write('\n')

