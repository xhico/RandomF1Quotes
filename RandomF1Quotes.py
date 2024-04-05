# -*- coding: utf-8 -*-
# !/usr/bin/python3

import logging
import os
import random
import traceback

import pandas as pd
import psutil
import tweepy
import yagmail

from Misc import get911


def tweet(tweetStr):
    """
    Posts a tweet to Twitter with the specified tweet string.

    Args:
        tweetStr (str): The tweet string to post.

    Returns:
        bool: True if the tweet was successfully posted, False otherwise.

    """
    try:
        # Use Tweepy API to post tweet
        api.update_status(tweetStr)

        # Log successful tweet
        logger.info("Tweeted")

        # Return True to indicate success
        return True
    except Exception as ex:
        # Log error if tweet fails
        logger.error(ex)

    # Return False to indicate failure
    return False


def getRandomQuote():
    """
    Returns a random quote and author from a CSV file.

    Returns:
        A tuple containing a random quote (string) and its author (string).
    """

    # get path to CSV file containing quotes
    csvFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Quotes.csv")

    # read CSV file into a pandas dataframe
    df = pd.read_csv(csvFile)

    # generate a random index between 0 and the number of quotes in the dataframe
    idx = random.randint(0, len(df))

    # retrieve the quote and author at the random index
    quote, author = df.loc[idx]["Quote"], df.loc[idx]["Author"]

    # return the quote and author as a tuple
    return quote, author


def favTweets(tags: str, numbTweets: int) -> bool:
    """
    Favorite tweets that match the given tags.

    Args:
        tags (str): A string of comma-separated tags to search for.
        numbTweets (int): The number of tweets to search and favorite.

    Returns:
        bool: True if the function completes successfully.

    Raises:
        None.

    Example:
        favTweets("python, data science", 10)

    """
    # Log that the function has been called
    logger.info("favTweets")

    # Replace spaces in the tags with "OR" for the Twitter API
    tags = tags.replace(" ", " OR ")

    # Use tweepy to search for tweets and store them in a list
    tweets = tweepy.Cursor(api.search_tweets, q=tags).items(numbTweets)
    tweets = [tw for tw in tweets]

    # Iterate over the tweets and favorite each one
    for tw in tweets:
        try:
            tw.favorite()
        except Exception as e:
            # If an error occurs, simply pass and move on to the next tweet
            pass

    # Return True to indicate that the function has completed successfully
    return True


def main():
    """
    Generate a random quote, set hashtags, reduce the quote length if necessary, tweet the quote,
    and like 10 recent tweets with the same hashtags.

    Preconditions:
    - Twitter API keys and access tokens are properly set up.
    - Tweepy library is installed.

    Postconditions:
    - A tweet is sent from the authenticated Twitter account with the random quote and hashtags.
    - The authenticated Twitter account likes 10 recent tweets with the same hashtags.
    """
    # Get quote | Set hashtags
    quote, author = getRandomQuote()  # retrieve a random quote and its author
    hashtags = "#F1 #Formula1 " + "#" + author.replace(" ", "")  # create hashtags with F1, Formula1, and the author's name as one word

    # Reduce quote if necessary
    if len("'" + quote + "' -" + author + hashtags) > 280:  # check if the quote, author, and hashtags exceed 280 characters (the Twitter limit)
        # shorten the quote to fit the limit, keeping room for the quote marks, the author, and the hashtags
        quote = quote[0:280 - len(quote) - (5 + 3) - len(author) - len(hashtags)] + "..."

    # Tweet!
    tweet("'" + quote + "' -" + author + " " + hashtags)  # tweet the quote, author, and hashtags with quote marks and a dash

    # Get tweets -> Like them
    favTweets(hashtags, 10)  # like the 10 most recent tweets that match the hashtags


if __name__ == "__main__":
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace('.py', '.log')}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

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

    # Check if script is already running
    procs = [proc for proc in psutil.process_iter(attrs=["cmdline"]) if os.path.basename(__file__) in '\t'.join(proc.info["cmdline"])]
    if len(procs) > 2:
        logger.info("isRunning")
    else:
        try:
            main()
        except Exception as ex:
            logger.error(traceback.format_exc())
            yagmail.SMTP(EMAIL_USER, EMAIL_APPPW).send(EMAIL_RECEIVER, "Error - " + os.path.basename(__file__), str(traceback.format_exc()))
        finally:
            logger.info("End")
