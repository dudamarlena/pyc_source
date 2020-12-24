# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/auth.py
# Compiled at: 2012-10-14 13:29:08
import tweepy
CONSUMER_KEY = '7it3IkPFI4RNIGhIci5w'
CONSUMER_SECRET = 'zGUE2bTucHcNn5IxFNyBP8dN2EvbrMtij5xuWHqcW0'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

def get_api():
    """ Authorize API to use user's account """
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'

    print 'Please go to the next URL and get your authorization number:\n %s' % redirect_url
    verifier = raw_input('Authorization Number:')
    token = auth.get_access_token(verifier)
    api = tweepy.API(auth)
    return api