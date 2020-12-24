# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tweethandler/setuputil.py
# Compiled at: 2010-04-29 03:55:24
import tweethandler
from tweepy import OAuthHandler

def run():
    print 'Input your application info.'
    consumer_key = raw_input('Consumer Key: ')
    consumer_secret = raw_input('Consumer Secret: ')
    auth = OAuthHandler(consumer_key, consumer_secret)
    print 'Visit the following url and allow TweetHandler to access.'
    print '>>> %s' % auth.get_authorization_url()
    print ''
    vcode = raw_input('Enter verification code: ')
    token = auth.get_access_token(vcode)
    print 'OK. You can setup TweetHander with following code.'
    print " ----\nfrom tweethandler import TweetHandler\nimport logging\nth = TweetHandler('%s',\n                  '%s',\n                  '%s',\n                  '%s')\n\nlogger = logging.getLogger()\nlogger.setLevel(logging.DEBUG)\nth.setLevel(logging.DEBUG)\nlogger.addHandler(th)\nlogger.info('Your log message')\n" % (consumer_key, consumer_secret,
     token.key, token.secret)