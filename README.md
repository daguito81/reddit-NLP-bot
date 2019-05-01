# reddit-NLP-bot
Bot to search comments in subreddits and provide sentiment analysis nad information

## Phase 1 (V1)
Script that catches negative comments in a specified subreddit.

Usage:
go into the Scripts folder
change the praw.ini file with your reddit app credentials
make sure you have a kafka broker running to catch the comments in json format
run `./run_instance [name_of_subreddit]`

The script will create a kafka topic with replication = 1 and partitions =1.  
If you want to run the script manually you can do: 
`python commentcather.py [name_of_subreddit]`.   
This will catch negative comments (less than -0.2 polarity) and send them to a kafka topic of the same name

## Phase 2 (TODO)
Create a callable bot that can respond by looking at a user history and calculate sentiment related metrics on their comments.  
Examples:
* How many comments
* Comment karma
* Avg karma / Comment
* % of Negative Comments
* Avg karma of negative comments
