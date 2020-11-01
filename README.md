# trp.red

 ** TO BE UPDATED **
 
For use with Turing trp.red project

a_get_raw_data.py:
	* Contains methods used to collect data from Pushshift API; if called from terminal, will collect all posts (a.k.a submissions) and comments for the subreddits listed in the `sudreddits.csv` file
	* To collect submissions for one subreddit at a time:
		*  get_submissions(subreddit, after, before, max_submissions = 200000000)
			* Parameters:
    				* **subreddit**: the subreddit that will be queried for submissions
    				* **after**: the start date or lower bound of the time period desired
				* **before**: the end date or upper bound of the time period desired 
			* This method also calls the `get_pages()` method within it which essentially "scrolls down" after each API query is made since you can only collect 500 items at a time (per Pushshift Github repo)
			
	* To collect comments:
		* get_comments(subreddit, before = None, after = None, max_comments = None)
			* Parameters: 
				* **subreddit**: the subreddit that will be queried for comments
				* **after**: he start date or lower bound of the time period desired
				* **before**: the end date or upper bound of the time period desired 
			* Unlike the submissions code, this method uses the PSAW module to collect comments (unsure why this method didn't work with submissions)
			
	


