import os
import praw






reddit = praw.Reddit(
  client_id = os.environ['client_id'],
  client_secret = os.environ['client_secret'],
  
  username = os.environ['username'],
  password = os.environ['password'],
  user_agent = "<ReplyCommentBot1.0>"
)


subreddit = reddit.subreddit("ProgrammerHumor")
for post in subreddit.hot(limit = 10):
  print(post.title)
