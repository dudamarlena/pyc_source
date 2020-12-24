# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_sentiment.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 2818 bytes
import unittest
from nltk.classify import SklearnClassifier

class TddInPythonExample(unittest.TestCase):

    def test_sentiment_variable_create_returns_correct_result(self):
        pos_tweets = [
         ('I love this car', 'positive'),
         ('This view is amazing', 'positive'),
         ('I feel great this morning', 'positive'),
         ('I am so excited about the concert', 'positive'),
         ('He is my best friend', 'positive'),
         ('This movie was great', 'positive'),
         ('This movie was not pathetic', 'positive')]
        neg_tweets = [
         ('I do not like this car', 'negative'),
         ('This view is horrible', 'negative'),
         ('I feel tired this morning', 'negative'),
         ('I am not looking forward to the concert', 'negative'),
         ('He is my enemy', 'negative'),
         ('This is a pathetic movie', 'negative')]
        tweets_with_sentiment = []
        for tweet, sentiment in pos_tweets + neg_tweets:
            filtered_tweet_words = [word.lower() for word in tweet.split() if len(word) >= 3]
            tweets_with_sentiment.append((filtered_tweet_words, sentiment))

        self.assertEqual([(['love', 'this', 'car'], 'positive'), (['this', 'view', 'amazing'], 'positive'), (['feel', 'great', 'this', 'morning'], 'positive'), (['excited', 'about', 'the', 'concert'], 'positive'), (['best', 'friend'], 'positive'), (['this', 'movie', 'was', 'great'], 'positive'), (['this', 'movie', 'was', 'not', 'pathetic'], 'positive'), (['not', 'like', 'this', 'car'], 'negative'), (['this', 'view', 'horrible'], 'negative'), (['feel', 'tired', 'this', 'morning'], 'negative'), (['not', 'looking', 'forward', 'the', 'concert'], 'negative'), (['enemy'], 'negative'), (['this', 'pathetic', 'movie'], 'negative')], tweets_with_sentiment)