# trp.red

 ** *TO BE UPDATED* **
 
For use with Turing trp.red project. Code written in python, except for network creation which was done in R.

## Document hierarchy
* Note that the code below assumes a certain document hierarchy:
```
trpred (git folder)
├── a_get_raw_data.py	# Code to collect data
├── b_clean_data.py	# Code to clean data
├── data               	# Data folder holding all raw and processed data
│   ├── raw         	# Raw data: output of a_get_raw_data.py
│   └── processed       # Processed data: output of b_clean_data.py
|       ├── submissions
|	|   ├── metadata
|	|   └── text
|	└── comments
|	    ├── metadata
|	    └── text
├── subreddits.csv	# A csv file that contains all of the subreddits of interest (i.e. those to be collected)
└── 
```

## a_get_raw_data.py:
* Contains methods used to collect data from Pushshift API
* If called from terminal, will collect all posts (a.k.a submissions) and comments for the subreddits listed in the `sudreddits.csv` file
### Submissions 
* To collect submissions for one subreddit at a time:
	*  get_submissions(subreddit, after, before, max_submissions = 200000000)
		* Parameters:
			* **subreddit**: the subreddit that will be queried for submissions
			* **after**: the start date or lower bound of the time period desired
			* **before**: the end date or upper bound of the time period desired 
			* This method also calls the `get_pages()` method within it which essentially "scrolls down" after each API query is made since you can only collect 1000 items at a time (per Pushshift Github repo)
		* Output:
			* A file of line separated json objects (where one line is one post)
### Comments		
* To collect comments for one subreddit at a time:
	* get_comments(subreddit, before = None, after = None, max_comments = None)
		* Parameters: 
			* **subreddit**: the subreddit that will be queried for comments
			* **after**: the start date or lower bound of the time period desired
			* **before**: the end date or upper bound of the time period desired 
		* Unlike the submissions code, this method uses the PSAW module to collect comments (unsure why this method didn't work with submissions)		
		* Output:
			* A file of line separated json objects (where one line is one comment)	
			
## b_clean_data.py
* Contains methods used to clean collected data. Given the size of some subreddits, I split up the data into two types -- metadata and text files
* Metadata files contain the fields of interest minus the text field which contains either the body of a post or comment (and is inherently bigger)
* The "fields of interest" that I keep in my clean data are specified by `keep_cols` (for metadata files) and `keep_cols_text` for text files in both the comments and submission methods
* If called from terminal, will `glob()` all the comments files and subsequently clean them, doing the same for submissions afterwards.  
### Submissions
* To clean submissions for one subreddit at a time:
	* clean_submissions(raw_submissions):
		* Parameters:
			* **raw_submissions**: the raw file of submissions that will be cleaned
		* Output:
			* A csv file where one row is one post and a column is a field of interest for that post
### Comments
* To clean submissions for one subreddit at a time:
	* clean_comments(raw_comments):
		* Parameters:
			* **raw_comments**: the raw file of comments that will be cleaned
		* Output:
			* A csv file where one row is one comment and a column is a field of interest for that comment

## utils.py
* TBU

# TBC...
