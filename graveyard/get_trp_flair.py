import numpy as np
import requests
import time
import pandas as pd
import json
import os

def get_trp_flair():
    # Get all trp users from submissions
    users_submissions = pd.read_csv(file_path, usecols = ["id","author"])

    # Get submission ids to search for author flair by submission
    ls_subids = list(users_submissions.id)

    counter = 0

    today = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d")

    if "submissions" in file_path:
        type = "submissions"

    else:
        type = "comments"

    filename = "data/info/" + today + "_" + type + "_trp_user_flairs.json"

    # initializing empty dict
    trpuser_flairs = {}

    for i in ls_subids:
        # set url to search by submission id
        url = "https://api.pushshift.io/reddit/submission/search/?ids="
        url = url + i # concat id from list
        r = requests.get(url) # make request

        author = users_submissions.loc[users_submissions['id'] == i]['author']
        author = author.values[0]

        try:
            flair = r.json()['data'][0]['author_flair_text'] # get flair if it exists
        except:
            flair = np.nan # otherwise, no flair

        trpuser_flairs[author] = flair

        print(i)
        counter += 1
        print("og start +:", counter)

        time.sleep(1)

        if len(trpuser_flairs.keys()) % 1000 == 0:
            try:
                with open(filename, 'wb') as outfile:
                    json.dump(trpuser_flairs, outfile)
            except:
                continue

if __name__ == "__main__"
    comment_file = "data/processed/comments/TheRedPill-metadata.csv"
    submission_file = "data/processed/submissions/TheRedPill-allsubmissions-2020-05-16-metadata.csv"
    get_trp_flair(comment_file)
    print("Flair from TRP comments done.")
    get_trp_flair("Flair from TRP submissions done.")
