from psaw import PushshiftAPI # https://github.com/dmarx/psaw
import datetime as dt
import pandas as pd
import all_scrape
import os

os.chdir("/Volumes/SAMSUNG/trpred")


# submission subeddits to get
missing_submissions = ['AskFeminists',
                         'fappeningdiscussion',
                         'fPUA',
                         'KotakuInAction',
                         'MGTOW2',
                         'RedPillReadingGroup',
                         'TumblrInAction',
                         'WhereAreAllTheGoodMen']

# comments to get
missing_comments = ["askanincel","masculism","fPUA","exredpill"]


#### TRIED TO USE PSAW - KEPT GETTING 429 ERRORS EVENT THOUGH THEY SHOULD MANAGE RATE LIMITS
# initialize api instance
# api = PushshiftAPI()


# get date limits
# start = int(dt.datetime(2012,10,25,0,0).timestamp())
# end = int(dt.datetime(2018,9,2,0,0).timestamp())
#
#
#
# # submission columns to keep
# keep_cols = ['id', 'created_utc', 'subreddit', 'author', 'title',
#               'score', 'num_comments', 'author_flair_text',
#               'selftext']
#
# ls_submissions = [] # will be list of dicts to write to JSON
#
# for i in missing_submissions:
#
#     # API call
#     gen = list(api.search_submissions(before = end,
#                                 after = start,
#                                 subreddit = i,
#                                 filter = keep_cols,
#                                 limit = None))
#     k = 0 # get accurate number of posts in a subreddit
#
#     for s in gen:
#         print(s)
#
#         break
#
#         ls_submissions.append(s) # append each submission to list (list of dicts)
#
#         if len(ls_submissions) == 10000: # save every 10k posts
#             k += 1
#             with open(filename, 'a', encoding='utf-8') as f: # write file
#                 json.dump(obj, f, ensure_ascii = False)
#                 f.write('\n')
#             print(k * 10000) # show progress
#
#     with open(filename, 'a', encoding='utf-8') as f: # write remaining posts
#         json.dump(obj, f, ensure_ascii = False)
#         f.write('\n')
######################

# for i in missing_submissions:
#     all_scrape.crawl_subreddit(i)

#### Get missing comments
# for i in missing_comments:
#     all_scrape.crawl_comments(i)



#### Try getting certain comments again using code
# Start date = date that r/trp was created
start = dt.datetime.strptime('2012-10-25', '%Y-%m-%d').date()
start_mod = 1533069478 # created_utc for last post collected

# End date = date that r/trp was quarantined
end = dt.datetime.strptime('2018-09-01', '%Y-%m-%d').date()


try_again_comments = ["MGTOW","IncelTears","exredpill","fPUA","masculism"]
for i in try_again_comments:
    print(i)
    if i == "MGTOW":
        start = start_mod
    else:
        start = dt.datetime.strptime('2012-10-25', '%Y-%m-%d').date()

    all_scrape.crawl_comments(i, after = start, before = end)
