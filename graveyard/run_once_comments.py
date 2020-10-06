import all_scrape as all
import datetime as dt
import pandas as pd
import os
import json
from dateutil.relativedelta import relativedelta


## Comments

# Get all comments
# all.crawl_comments("TheRedPill")


# Get comments for ancillary subreddits
subreddits = [\
             #    "RedPillWomen",\
             #    "askTRP",\
             #    "RedPillParenting",\
             #    "thankTRP",\
             #    "RedPillLit",\
             #    "becomeaman",\
             #    "altTRP",\
             #    "GEOTRP",\
             #    "TRPOffTopic",\
             #     "u_TRP_Scepter",\
             #     "RedPillNonMonogamy",\
             #     "RedPillWives",\
             #     "redpillfatherhood",\
             #     "redpillbooks",\
             #     "RedPillWorkplace",\
             #     "theRedPillLeft",\
             #     "TRPmemes",\
             #     "theredpillright",\
             #     "EthnicRedPill",\
             #     "marriedredpill",\
             # "AskFeminists", "askseddit", "badwomensanatomy",\
             #  "Egalitarianism", "exredpill", "FeMRADebates",\
             #  "GEOTRP", "IncelsInAction", "IncelsWithoutHate",\
             #  "masculism", "MensRants",\
              # "MensRights",\
             # "mensrightslaw",\
             #  "MensRightsMeta",\
              # "MGTOW"\
              # "mgtowbooks","MRActivism",\
              # "NOMAAM", "pua", "PurplePillDebate", "seduction", "Trufemcels"\
              ]
for s in subreddits:
     all.crawl_comments(s)
     print(s+" done")
