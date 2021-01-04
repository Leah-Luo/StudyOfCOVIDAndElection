# coding: utf-8
"""
  This file is used to extract tweets based on hashtags of presidential condicates. 
  Extracting data every day and append to the same csv file.
  The data only focuses on the United States. 
"""

import tweepy
import twitter
import emoji
import time
import csv
from datetime import datetime 
import pandas as pd
import numpy as np
import os


CONSUMER_KEY = 'ezlnFsruPcfpep9GAjTi14n4c'
CONSUMER_SECRET = 'nzU3Hc9HLrYBQZCprRwz57KUZyGbUIrp6nvOQoEHUrMUsgwdKV'
OAUTH_TOKEN = '1237146504432926721-QZdMsNwwNoPkmtc1DdvcjpUiG9lAB8'
OAUTH_TOKEN_SECRET = 'bINg1R99FiaNSulhD1WoxnbYTUxyfRafshKwN9BIYWAZh'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

authT = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
authT.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(authT)

# The area of tweets focuses on USA
places = api.geo_search(query="USA", granularity="country")
place_id = places[0].id


# All states have state code with same index
states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
          "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
          "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
          "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
          "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
          "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
          "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
          "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

states_code = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]




# Save dataframe into csv file
def saveFile(df):
    csv = 'Data/Dataset.csv'
    
    # Create new csv file if it does not exist
    if not os.path.isfile(csv):
        df.to_csv(csv, header=True, index=False, encoding='utf-8')
        print("New File Created")
    # Append data to exist csv file
    else:
        df.to_csv(csv, mode='a', header=False, index=False)
        print("Append data to Existing File")


# Save list attributes into dataframe
def saveFrame(created_at, tweet, state, state_code):
    colName = ['created_at', 'tweet', 'state', 'state_code']
    df = pd.DataFrame(columns = colName)
    
    df['created_at'] = created_at
    df['tweet'] = tweet
    df['state'] = state
    df['state_code'] = state_code

    saveFile(df)


# Extract tweets from tweepy cursor
def extractTweets(tweets, name):
    cnt = 0

    for tweet in tweets:
        # Remove Emoji
        text = ''.join(c for c in tweet.full_text if c not in emoji.UNICODE_EMOJI)    

        for i in range(len(states)):
            if (states[i] in tweet.place.full_name) or (states_code[i] in tweet.place.full_name):
                time.append(now)
                data.append(text)
                state.append(states[i])
                stateCode.append(states_code[i])
                cnt+=1


    print(name + ': ', cnt)
    saveFrame(time, data, state, stateCode)


data = []
time = []
state = []
stateCode = []

# The time is the date of extracting tweets
now = datetime.now().strftime("%m/%d/%Y")

# Hashtags related to DonaldTrump & JoeBiden
q_trump = '{} place:{}'.format("#DonaldTrump", place_id)
q_biden = '{} place:{}'.format("#JoeBiden", place_id)

# Extract tweets in U.S. by hashtag 
tweets_trump = tweepy.Cursor(api.search, q = q_trump, lang="en", include_rts = False, tweet_mode = 'extended').items(1000)
tweets_biden = tweepy.Cursor(api.search, q = q_biden, lang="en", include_rts = False, tweet_mode = 'extended').items(1000)


extractTweets(tweets_trump, 'Trump')
extractTweets(tweets_biden, 'Biden')


