import nltk
from textblob import TextBlob
import pandas as pd
import time
import praw
import sys
from kafka import SimpleProducer, KafkaClient

reddit = praw.Reddit('test-bot')
subreddit = reddit.subreddit(sys.argv[1])


results = pd.DataFrame()
#results = pd.DataFrame(columns=['Comment_ID', 'Body', 'Controversiality', 'Comment_Date',
#                                'Comment_Score', 'Polarity', 'Subjectivity',
#                                'Author', 'Author_flair_text', 'Author_LKarma', 'Author_CKarma', 'Author_Date',
#                                'Submission_ID', 'Submission_title', 'Submission_Date',
#                                'Submission_Title_Polarity', 'Submission_Title_Subjectivity',
#                                'Submission_Score', 'Submission_Author', 'Submission_Author_LKarma',
#                                'Submission_Author_CKarma', 'Submission_Author_Date', 'Subreddit',
#                                ])

kafka = KafkaClient(["localhost:9092", "localhost:9093"])
producer = SimpleProducer(kafka)

i = len(results)
for comment_tracker in subreddit.stream.comments():

    comment_sentiment = TextBlob(comment_tracker.body).sentiment
    thread_title_sentimet = TextBlob(comment_tracker.submission.title).sentiment

    if comment_sentiment[0] < -0.2:
        print("---------------------------------")
        print("Found a negative comment")
        print("Author: ", comment_tracker.author)
        print("Body: ", comment_tracker.body)
        print("Comment Karma: ", comment_tracker.author.comment_karma)

        results.loc[i, 'Comment_ID'] = comment_tracker.id
        results.loc[i, 'Body'] = comment_tracker.body
        results.loc[i, 'Controversiality'] = comment_tracker.controversiality
        results.loc[i, 'Comment_Date'] = comment_tracker.created_utc
        results.loc[i, 'Comment_Score'] = comment_tracker.score
        results.loc[i, 'Polarity'] = comment_sentiment[0]
        results.loc[i, 'Subjectivity'] = comment_sentiment[1]

        results.loc[i, 'Author'] = comment_tracker.author.name
        results.loc[i, 'Author_flair_text'] = comment_tracker.author_flair_text
        results.loc[i, 'Author_LKarma'] = comment_tracker.author.link_karma
        results.loc[i, 'Author_CKarma'] = comment_tracker.author.comment_karma
        results.loc[i, 'Author_Date'] = comment_tracker.author.created_utc

        results.loc[i, 'Submission_ID'] = comment_tracker.submission.id
        results.loc[i, 'Submission_title'] = comment_tracker.submission.title
        results.loc[i, 'Submission_Date'] = comment_tracker.submission.created_utc
        results.loc[i, 'Submission_Title_Polarity'] = thread_title_sentimet[0]
        results.loc[i, 'Submission_Title_Subjectivity'] = thread_title_sentimet[1]
        results.loc[i, 'Submission_Score'] = comment_tracker.submission.score

        results.loc[i, 'Submission_Author'] = comment_tracker.submission.author.name
        results.loc[i, 'Submission_Author_LKarma'] = comment_tracker.submission.author.link_karma
        results.loc[i, 'Submission_Author_CKarma'] = comment_tracker.submission.author.comment_karma
        results.loc[i, 'Submission_Author_Date'] = comment_tracker.submission.author.created_utc
        results.loc[i, 'Subreddit'] = comment_tracker.subreddit.display_name

        producer.send_messages(sys.argv[1], results.loc[i].to_json().encode('utf-8'))
        print("---------JSON---------")
        print(results.loc[i].to_json())
        i += 1
 #       if i > int(sys.argv[2]):
 #           break


# print(results.head())
