import a_get_raw_data as get_raw
import b_clean_data as clean
import utils
import os
import pandas as pd

os.chdir("/Volumes/SAMSUNG/trpred")

# Braincels POSTS has date gap from 2018-07-17 to 2018-09-01
get_raw.get_comments("Braincels", after = str(utils.get_startdate()), before = "1515257386")


# Get mensrights comments that are missing
# get_raw.get_comments("MensRights", after = str(utils.get_startdate()), before = "1397692800")

# file = "data/raw/submissions/Braincels-allsubmissions-2020-10-19.json"

# clean.clean_submissions(file)

# df_comments = utils.count_processedentries("comments")
#
# df_comments.to_csv("data/info/20201019_comments_collected_counted.csv")

# # Clean file KIA file
# files = ["/Volumes/SAMSUNG/trpred/data/raw/comments/KotakuInAction-allcomments-2020-10-06.json"
#
# df_totals = pd.DataFrame(columns = ['subreddit', 'total'])
#
# if data_type == "comments":
#     files = glob.glob("data/processed/comments/*-metadata.csv")
#
#
# elif data_type == "submissions":
#     files = glob.glob("data/processed/submissions/*-metadata.csv")
#
# else:
#     raise ValueError("Invalid data_type: must be either 'comments' or 'submissions'")
#
# for i in files:
#     # get name of subreddit from file name
#     regex = r"^.*\/([^-]*)-.*$"
#     matches = re.search(regex, i)
#     subreddit = matches.group(1)
#
#     # get the length of the file using helper function
#     total = file_len(i)
#
#     df_totals = df_totals.append({'subreddit':subreddit, 'total':total}, ignore_index = True)
