import all.py as all
import os

### SUBMISSIONS ###

# Get number of submissions in entire subreddit
# requests.get(url, params = {"subreddit": "TheRedPill", "size": 0, "aggs" : "subreddit"}).json()["aggs"]
# Result (May 15th): 112,196 posts in the entire subreddit

# Get submissions
submissions = all.crawl_subreddit("TheRedPill")

# Save data as .json

# Get date
today = dt.datetime.utcnow().date()

os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing Institute/trpred/data/raw/submissions") # change wd
filename = "submissions-" + str(today) + ".json" # create filename

with open(filename, 'w', encoding='utf-8') as f: # write file
    json.dump(submissions, f, ensure_ascii = False, indent=4)


# Get comments
df_comments = all.crawl_comments('TheRedPill')

# Save data as .json
os.chdir("/Users/mariajoseherrera/Documents/Admin/yahb/Turing Institute/trpred/data/raw/comments")# change wd
filename = "comments-" + str(today) + ".json" # create filename

df_comments.to_json(filename)
