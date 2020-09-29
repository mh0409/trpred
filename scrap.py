import clean as clean
import os
import re
import glob
import csv
from fsplit.filesplit import FileSplit

os.chdir("/Volumes/SAMSUNG/trpred")

# Function will tell you file name, size in bytes, and line count
def func(f, s, c):
    print("file: {0}, size: {1}, count: {2}".format(f, s, c))

##### CHUNK 1: SPLIT R/TRP COMMENT FILE INTO MANY FILES AND CLEAN

# filenames = ["TheRedPill-allcomments-2020-09-23"]
#
#
#
# for i in filenames:
#     file_path = "/Volumes/SAMSUNG/trpred/data/raw/comments/" + i + ".json"
#     folder_path = "/Volumes/SAMSUNG/trpred/data/raw/comments/" + i + "/"
#
#     os.chdir("/Volumes/SAMSUNG/trpred")
#     dir = os.listdir(folder_path)
#
#     # If folder is empty (i.e. file hasn't been split yet)...
#     if len(dir) == 0:
#
#         # ...then split file
#         fs = FileSplit(file = file_path, splitsize = 15000000, output_dir = folder_path)
#
#         fs.split(callback = func)
#
# subreddit_folders = "/Volumes/SAMSUNG/trpred/data/raw/comments/TheRedPill-allcomments-2020-09-23"

# Pass in folder name to method
# clean.clean_comments(subreddit_folders)
# print(i + " complete")

###### CHUNK 2: CHECK TO SEE WHAT INDEX R/SEDUCTION WAS
# subreddit_folders = [x[0] for x in os.walk("data/raw/comments")]
#
# print(*subreddit_folders, sep = "\n")
# print(subreddit_folders[-3:]) # so this is the index i need to clean the remaining comment subreds
################


##### CHUNK 3: FIGURE OUT WHAT COMMENTS NEED TO BE gotten
# # Read in all subreddits
# subreddits = []
#
# with open('subreddits.csv', newline='') as f:
#     reader = csv.reader(f)
#     for row in reader:
#             subreddits.append(row)
#
# # Subreddits hold the final list of subreddits we expect to have
# all_subreddits = list(set([x for x in subreddits[0]]))
#
# # See what I have
# raw_comments = glob.glob("data/raw/comments/*.json")
# raw_comments = list(dict.fromkeys(raw_comments))
#
# raw_ls = []
#
# # get subreddit names
# for i in raw_comments:
#     regex = r"^.*\/([^-]*)-.*$"
#     matches = re.search(regex, i)
#     subreddit = matches.group(1)
#     raw_ls.append(subreddit)
#
# comments_tocollect = list(set(all_subreddits)-set(raw_ls))
#
# with open('missing_comments.csv', 'w', newline='') as out_f:
#     w = csv.writer(out_f)
#     w.writerow(comments_tocollect)
### SAVED!!!

###### CHUNK 4:  CLEAN SUBMISSIONS #####

# ls_raw = ["askanincel-allcomments-2020-09-27.json",
#  "exredpill-allcomments-2020-09-27.json",
#  "fPUA-allcomments-2020-09-27.json",
#  "masculism-allcomments-2020-09-27.json",
#  "TumblrInAction-allcomments-2020-09-27.json"]
#
# # 0) Get name of subreddit
# regex = r"([^\/]+)(?=\.json$)"
#
# filenames = []
#
# for i in ls_raw:
#  matches = re.search(regex, i)
#  new_file = matches.group()
#  filenames.append(new_file)
#
# # 1) Create folders
# for i in filenames:
#     path = "data/raw/comments/" + i
#
#     try:
#         os.mkdir(path)
#     except OSError:
#         print ("Creation of the directory %s failed" % path)
#     else:
#         print ("Successfully created the directory %s" % path)
#
# # 2) ...and split files
# for i in filenames:
#     file_path = "/Volumes/SAMSUNG/trpred/data/raw/comments/" + i + ".json"
#     folder_path = "/Volumes/SAMSUNG/trpred/data/raw/comments/" + i + "/"
#
#     os.chdir("/Volumes/SAMSUNG/trpred")
#     dir = os.listdir(folder_path)
#
#     # If folder is empty (i.e. file hasn't been split yet)...
#     if len(dir) == 0:
#
#         # ...then split file
#         fs = FileSplit(file = file_path, splitsize = 15000000, output_dir = folder_path)
#
#         fs.split(callback = func)
#
#


# 3) Clean files

# # Pass in folder name to method
# subreddit_folders = ["/Volumes/SAMSUNG/trpred/data/raw/comments/askanincel-allcomments-2020-09-27",
# "/Volumes/SAMSUNG/trpred/data/raw/comments/exredpill-allcomments-2020-09-27",
# "/Volumes/SAMSUNG/trpred/data/raw/comments/fPUA-allcomments-2020-09-27",
# "/Volumes/SAMSUNG/trpred/data/raw/comments/masculism-allcomments-2020-09-27",
# "/Volumes/SAMSUNG/trpred/data/raw/comments/TumblrInAction-allcomments-2020-09-27"]
#
# for i in subreddit_folders:
#     clean.clean_comments(i)
#     print(i + " complete")
#
#
#
########################################


#### CHUNK : Process Submissions:
ls_subs = ["/Volumes/SAMSUNG/trpred/data/raw/submissions/TumblrInAction-allsubmissions-2020-09-27.json"]

for i in ls_subs:
    clean.clean_subreddit(i, "submissions")
    print(i+" complete")
