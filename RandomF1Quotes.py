# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install tweepy pandas --no-cache-dir

import json
import os
import random

import pandas as pd
import tweepy
import yagmail


def get911(key):
    f = open('/home/pi/.911')
    data = json.load(f)
    f.close()
    return data[key]


CONSUMER_KEY = get911('TWITTER_F1_CONSUMER_KEY')
CONSUMER_SECRET = get911('TWITTER_F1_CONSUMER_SECRET')
ACCESS_TOKEN = get911('TWITTER_F1_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = get911('TWITTER_F1_ACCESS_TOKEN_SECRET')
EMAIL_USER = get911('EMAIL_USER')
EMAIL_APPPW = get911('EMAIL_APPPW')
EMAIL_RECEIVER = get911('EMAIL_RECEIVER')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def tweet(str):
    api.update_status(str)
    print("Tweeted - " + str)

    return True


def getRandomQuote():
    csvFile = "Quotes.csv"
    df = pd.read_csv(csvFile)
    idx = random.randint(0, len(df))

    quote, author = df.loc[idx]["Quote"], df.loc[idx]["Author"]
    return quote, author


if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print("Login as: " + api.verify_credentials().screen_name)

        quote, author = getRandomQuote()
        hashtags = "#F1 #Formula1 " + "#" + author.replace(" ", "")

        if len("'" + quote + "' -" + author + hashtags) > 280:
            quote = quote[0:280 - len(quote) - (5 + 3) - len(author) - len(hashtags)] + "..."

        tweetStr = "'" + quote + "' -" + author + " " + hashtags
        tweet(tweetStr)
    except Exception as ex:
        print(ex)
        yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, "Error - RandomF1Quotes", str(ex))
