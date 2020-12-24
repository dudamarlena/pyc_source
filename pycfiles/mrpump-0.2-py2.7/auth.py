# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/auth.py
# Compiled at: 2012-05-05 15:27:56
import tweepy

def get_api(config):
    consumer_key = config.get('app', 'key')
    consumer_secret = config.get('app', 'secret')
    me = config.get('global', 'screen name')
    me_oauth_token = config.get(me, 'token')
    me_oauth_secret = config.get(me, 'secret')
    oa = tweepy.OAuthHandler(consumer_key, consumer_secret)
    oa.set_access_token(me_oauth_token, me_oauth_secret)
    api = tweepy.API(oa)
    return api