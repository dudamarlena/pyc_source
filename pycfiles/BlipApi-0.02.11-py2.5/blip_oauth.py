# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/blip_oauth.py
# Compiled at: 2010-05-29 17:02:01
CONSUMER_KEY = '9IIoLsjrHKW9cAIePhvw'
CONSUMER_SECRET = 'YMk75YklVYnwAYDllJP2WM2H8ktZFBUN2fumv5K6'
from oauth import oauth
from blipapi import BlipApi
consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
access_token = oauth.OAuthToken.from_string('oauth_token_secret=.....................&oauth_token=................')
api = BlipApi(oauth_token=access_token, oauth_consumer=oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET))
print api.dashboard_read(limit=1)
print
print api.dirmsg_create('dirmsg test', 'mrk')