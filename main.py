import os
import praw
import csv
import re
from datetime import datetime


reddit = praw.Reddit(
  client_id = os.environ['client_id'],
  client_secret = os.environ['client_secret'],
  
  username = os.environ['username'],
  password = os.environ['password'],
  user_agent = "<thisshouldwork>"
)

def clean(raw_string):
  clean = raw_string.lower()
  clean = re.sub(r'[^A-Za-z0-9 ]+', '', clean)
  return clean

class RedditBot:
  def __init__(self, filename): 
    self.response_list = []
    with open(filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter = ",")
      for row in csv_reader:
        self.response_list.append({'phrase': clean(row[0]),
                                  'reply': clean(row[1])
         })
      
  def find_match(self, comment):
    for i, dictionary in enumerate(self.response_list):
        if dictionary['phrase'] in clean(comment.body):
          if self.cooled_down(i):
            self.make_reply(i, comment)
         


  def cooled_down(self, i):
    dictionary = self.response_list[i]
    if 'last_posted' not in dictionary.keys():
      return True
    else:
      now = datetime.now()
      duration = now - datetime.fromtimestamp(dictionary['last_posted'])
      duration_seconds = duration.total_seconds()
      hours = divmod(duration_seconds, 3600)[0]
      if hours >= 24:
        return True
      else:
        print(f"Couldn't post {dictionary['phrase']} Cool Down time: {24 - hours}")
        

  def make_reply(self, i, comment):
    dictionary = self.response_list[i]
    try:
      comment.reply(dictionary['reply'])
      print(comment.body)
      print(dictionary['phrase'])
      print(dictionary['reply'])
    except Exception as e:
      print(e)




bot = RedditBot("pairs.csv")
subreddit = reddit.subreddit("testing__bot")
for comment in subreddit.stream.comments(skip_existing=True):
   bot.find_match(comment)