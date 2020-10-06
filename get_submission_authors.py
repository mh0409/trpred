import re
from glob import glob
import pandas as pd

# Unique users per subreddits

# Load in one example
file_subs = glob("data/processed/submissions/*metadata.csv")

df_allauthors = pd.DataFrame(columns=['author', 'subreddit'])

for i in file_subs:
    df_subs = pd.read_csv(i)

    # Frequency per author -- get top 100
    n = 10
    df_subs.author.value_counts().head(50) # limit to top n; output: pandas series

    # get name of subreddit from file name
    regex = r"^.*\/([^-]*)-.*$"
    matches = re.search(regex, i)
    subreddit = matches.group(1)

    ## per posts
    authors_submissions = df_subs.author.unique()

    df_authors = pd.DataFrame({'author': authors_submissions})
    df_authors['subreddit'] = subreddit


    df_allauthors = pd.concat([df_allauthors, df_authors])
    df_authors = pd.DataFrame()

new_file = "data/processed/submissions/authors.csv"
df_allauthors.to_csv(new_file, mode = "w") # mode= w will overwrite previous file
