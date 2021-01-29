# -*- coding: utf-8 -*-
# !/usr/bin/python3

# pip3 install tweepy animals.py schedule

import os
import pytz
import time
import tweepy
import schedule
import urllib.request
from random import randint
from animals import Animals
from datetime import datetime


def oauthLogin():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    print("Authenticated as: %s" % api.me().screen_name)
    
    return api
      

def tweet(api, str, img, replyId):
    try:
        if img != "":
            api.update_with_media(img, str)
        elif replyId != 0:
            api.update_status('Have a nice day!', replyId, auto_populate_reply_metadata = True)
        else:
            api.update_status(str)
        print("Tweeted")
        
    except Exception as inst:
        print("Failed to Tweet")
        print(inst)
        return False
    
    return True
    
    
def batchDelete(api):
    for tw in tweepy.Cursor(api.user_timeline).items():
        try:
            print("Deleting ID: " + str(tw.id) + " - ", end =" ")
            api.destroy_status(tw.id)
            print("Deleted")
        except Exception as inst:
            print("Failed to Delete")
    
    return True


def getAnimal(dirName):
    animal = Animals('cat')
    imgUrl = animal.image()
    imgFact = animal.fact()
    imgFilename = os.path.join(dirName, str(randint(1, 999)) + ".jpg")
    
    urllib.request.urlretrieve(imgUrl, imgFilename)

    return imgFilename
    

def deleteJPG(dirName):
    for file in os.listdir(dirName):
        if file.endswith(".jpg"):
            os.remove(file)
    
    return True


def getLastTweet(api, userName):
    tweet = api.user_timeline(screen_name = userName, count = 1, include_rts = False, exclude_replies = True)[0]
    now = datetime.now()
    if str(tweet.created_at) < str(now.strftime("%Y-%m-%d %H:%M:%S")):
        return tweet.id
    
    return 0
    

if __name__ == "__main__":
    myDir = os.getcwd()
    myAPI = oauthLogin()
    
    tweet(myAPI, "Hallo", "", 0)
    #batchDelete(myAPI)
    #deleteJPG(myDir)
    

    
    
    
    