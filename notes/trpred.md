* [x] Clean braincels comments

* [x] Clean mensrights comments

* [x] Set up submissions table on athena

* [x] Set up comments table on athena

* [ ] Add structure to repo

* [ ] Write up subreddits of interest in Google Doc

  * As if it were a paper

* [ ] Write up data collection procedure in Google Doc

* [ ] Update Athena files with new comments / submission docs

* [ ] Create Notion docs for people to use /set up Athena

  * [ ] Can 2 databases speak to each other?
    * Add sample query to look both at DB
  * [ ] Can we export Athena tables / save down?
  * [ ] Can we edit in R?
  * [ ] Share S3 bucket - set up role?
  * [ ] Transfer ownership of account to Bertie (bertievidgen@gmail.com)

* [ ] Update code to split up files in the same way as needed for athena

* [ ] Share Athena database

* [ ] Rerun clean for all comments to get `link_id` which links comments to submission

* [ ] How to squash comments/posts together?

  * [ ] Add type column (comments/post) so we can differentiate between them if we wanna combine

* [ ] Add process to readme

  1) Scrape files

  2) clean

  3) upload to aws s3

  4) create athena database

  5) export results

* [ ] Set up Athena database

  * [ ] Manifest? or can Athena just take all files in one folder?
    * Can do this directly on the site? maybe just need to click on `create table` and do it from there (use a preview of the processed csv to get column names)
    * Need 1 metadata table and 1 text table for comments and submissions each
  * [ ] Can we export it?
    * [ ] Create documentation around how to do it
    * [ ] How big is the file?

* Compare vs API pull numbers
  
  * Reconcile
    * Submissions: Braincels is way off -- organize processed data and see what dates were collected
      * [x] Braincels POSTS has date gap from 2018-07-17 to 2018-09-0
        * [x] Pull missing dates
        * [x] Combine old file with new file
        * [x] Re-clean
  
* Look into weird comment discrepancies
  - [x] Check on MGTOW missing comments pull (in iterm)
    * [x] Combine with old MGTOW comment file
    * [x] Reclean
    * [x] Check for duplicates
    * [x] Check count
  - [x] Rerun Braincels missing dates pull
    * [x]  Braincels POSTS has date gap from 2018-07-17 to 2018-09-01  -- set up in scrap doc
    * [x] **Merge with old braincels**
    * [x] Clean
    * [x] Remove dupes
    * [x] Recount
  - [x] Load in ID column from any subreddits that have too many entries and see if any dupes: 
    - [x] RUN DEDUPE() FUNCTION IN SANDBOX2 FOR THE BELOW SUBREDDS (COMMENTS)
    - [x] WhereAreAllTheGoodMen COMMENTS
    - [x] GEOTRP
      - [x] Use this for trial - load in csv and see how to remove duplicate rows based on "id"
    - [x] Braincels COMMENTS
    - [x] MensRights COMMENTS
    - [x] KotakuInAction COMMENTS

* Make github public

  - [ ] Update readme
  - [ ] Clean up scraping / cleaning code

* Descriptive Stats

  - [ ] Expand descriptive stats code for all subreddits?
  - [ ] Create desc stats for overall subredddits (see jupyter nb)

- [ ] Clean up submissions raw data collection -- I think I'm doing something wrong w/ earliest and last posttime arguments in get_pages
  - [ ] Look into the concept of "scrolling" (i.e. picking up from where the last request stopped)

- [ ] clean all submissions again
  - [x] Need to add date formatting back into code since need it for mask
  - [x] Refine clean_submissions() in JupyterNB (processing2) and migrate back into atom
  - [ ] Move df_author code to atom (processing2)
  - [ ] Move subreddit counts code to atom (processing2)
  - [x] Get counts for processed posts and compare vs API
- [x] Repull Kotaku In Action and MGTOW
  * Also, organize the processed files by date, re-save, and see if i can discern the dates that are missing

- [x] Test clean_submissions