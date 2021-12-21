# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install tweepy pandas --no-cache-dir

import os
import sys
import time
import json
import tweepy
import random
import pandas as pd


def get911(key):
    f = open('/home/pi/.911')
    data = json.load(f)
    f.close()
    return data[key]


CONSUMER_KEY = get911('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = get911('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = get911('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = get911('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        print(status.text)


def tweet(str):
    try:
        api.update_status(str)
        print("Tweeted - " + str)
    except:
        print("Failed to Tweet - " + str)
        return False

    return True


def batchDelete():
    for tw in tweepy.Cursor(api.user_timeline).items():
        try:
            print("Deleting ID: " + str(tw.id) + " - ", end=" ")
            api.destroy_status(tw.id)
        except:
            print("Failed to Delete")
            pass

    return True


def follow(usernames):
    userIDs = [api.get_user(
        screen_name=username).id_str for username in usernames]

    printer = IDPrinter(CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    printer.filter(follow=userIDs)

    return True


def getRandomQuote():
    csvFile = "Quotes.csv"
    df = pd.read_csv(csvFile)
    idx = random.randint(0, len(df))

    quote, author = df.loc[idx]["Quote"], df.loc[idx]["Author"]
    return quote, author


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Login as: " + api.verify_credentials().screen_name)

    # Get op Arg
    try:
        # Get mode from arg
        op = sys.argv[1]
        if op == "--tweet" or op == "-t":
            tweet(sys.argv[2])
        elif op == "--delete" or op == "-d":
            batchDelete()
    except:
        quote, author = getRandomQuote()
        hashtags = "#F1 #Formula1 " + "#" + author.replace(" ", "")

        if len("'" + quote + "' -" + author + hashtags) > 280:
            quote = quote[0:280 - len(quote) -
                          (5 + 3) - len(author) - len(hashtags)] + "..."

        tweetStr = "'" + quote + "' -" + author + " " + hashtags
        tweet(tweetStr)
