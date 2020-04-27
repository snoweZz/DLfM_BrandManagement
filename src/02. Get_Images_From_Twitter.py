# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:55:42 2020

@author: lsamsi
"""

# based on: https://miguelmalvarez.com/2015/03/03/download-the-pictures-from-a-twitter-feed-using-python/

# Important Note: there are rate limits in the use of the Twitter API, as well as limitations in case you want to provide a downloadable data-set
# 1. register a Twitter App at developer.twitter.com by setting up a twitter developer account 

import tweepy
from tweepy import OAuthHandler
import json
 
consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'
 
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


tweets = api.user_timeline(screen_name='miguelmalvarez',
                           count=200, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id
 
while (True):
    more_tweets = api.user_timeline(screen_name=username,
                                count=200,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)
# There are no more tweets
if (len(more_tweets) == 0):
      break
else:
      last_id = more_tweets[-1].id-1
      tweets = tweets + more_tweets
      
media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])

import wget
...
 
for media_file in media_files:
    wget.download(media_file)        