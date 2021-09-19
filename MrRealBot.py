# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install tweepy --no-cache-dir

import os
import time
import tweepy
from dotenv import load_dotenv
load_dotenv()

debug = True


def oauthLogin():
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    if debug:
        print("Authenticated as: %s" % api.me().screen_name)

    return api


def tweet(api, str):
    try:
        api.update_status(str)
        if debug:
            print("Tweeted - " + str)
    except:
        if debug:
            print("Failed to Tweet - " + str)
        return False

    return True


def batchDelete(api):
    for tw in tweepy.Cursor(api.user_timeline).items():
        try:
            if debug:
                print("Deleting ID: " + str(tw.id) + " - ", end=" ")
            api.destroy_status(tw.id)
            if debug:
                print("Deleted")
        except:
            if debug:
                print("Failed to Delete")

    return True


def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "").rstrip()
    return temp


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    myAPI = oauthLogin()

    batchDelete(myAPI)
    # piTemp = "Raspberry Pi Temperature: " + measure_temp()
    # tweet(myAPI, piTemp)
