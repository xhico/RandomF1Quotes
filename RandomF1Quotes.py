# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install tweepy yagmail pandas python-dateutil psutil --no-cache-dir
import datetime
import json
import os
import random
import psutil
import pandas as pd
import tweepy
import yagmail
import traceback


def get911(key):
    with open('/home/pi/.911') as f:
        data = json.load(f)
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


def tweet(tweetStr):
    try:
        api.update_status(tweetStr)
        print("Tweeted")
        return True
    except Exception as ex:
        print(ex)
        print("Failed")
    return False


def getRandomQuote():
    csvFile = "Quotes.csv"
    df = pd.read_csv(csvFile)
    idx = random.randint(0, len(df))

    quote, author = df.loc[idx]["Quote"], df.loc[idx]["Author"]
    return quote, author


def favTweets(tags, numbTweets):
    print("favTweets")
    tags = tags.replace(" ", " OR ")
    tweets = tweepy.Cursor(api.search_tweets, q=tags).items(numbTweets)
    tweets = [tw for tw in tweets]

    for tw in tweets:
        try:
            tw.favorite()
        except Exception as e:
            pass

    return True


def main():
    # Get quote | Set hashtags
    quote, author = getRandomQuote()
    hashtags = "#F1 #Formula1 " + "#" + author.replace(" ", "")

    # Reduce quote if necessary
    if len("'" + quote + "' -" + author + hashtags) > 280:
        quote = quote[0:280 - len(quote) - (5 + 3) - len(author) - len(hashtags)] + "..."

    # Tweet!
    tweet("'" + quote + "' -" + author + " " + hashtags)

    # Get tweets -> Like them
    favTweets(hashtags, 10)


if __name__ == "__main__":
    print("----------------------------------------------------")
    print(str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if script is already running
    procs = [proc for proc in psutil.process_iter(attrs=["cmdline"]) if os.path.basename(__file__) in '\t'.join(proc.info["cmdline"])]
    if len(procs) > 2:
        print("isRunning")
    else:
        try:
            main()
        except Exception as ex:
            print(traceback.format_exc())
            yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, "Error - " + os.path.basename(__file__), str(traceback.format_exc()))
        finally:
            print("End")
