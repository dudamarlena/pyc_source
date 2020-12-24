# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/api.py
# Compiled at: 2016-02-11 09:18:14
from datetime import datetime
import sys
from django.conf import settings
from oauth_tokens.api import ApiAbstractBase, Singleton
from oauth_tokens.models import AccessToken
from tweepy import TweepError as TwitterError
import tweepy
__all__ = [
 'api_call', 'TwitterError']
TWITTER_CLIENT_ID = getattr(settings, 'OAUTH_TOKENS_TWITTER_CLIENT_ID', None)
TWITTER_CLIENT_SECRET = getattr(settings, 'OAUTH_TOKENS_TWITTER_CLIENT_SECRET', None)

@property
def code(self):
    if 'code' in self[0][0]:
        return self[0][0]['code']
    return 0


TwitterError.code = code

class TwitterApi(ApiAbstractBase):
    __metaclass__ = Singleton
    provider = 'twitter'
    error_class = TwitterError
    sleep_repeat_error_messages = [
     'Failed to send request:']

    def get_consistent_token(self):
        return getattr(settings, 'TWITTER_API_ACCESS_TOKEN', None)

    def get_api(self, token):
        delimeter = AccessToken.objects.get_token_class(self.provider).delimeter
        auth = tweepy.OAuthHandler(TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET)
        auth.set_access_token(*token.split(delimeter))
        return tweepy.API(auth, wait_on_rate_limit=True, retry_count=3, retry_delay=1, retry_errors=set([401, 404, 500, 503]))

    def get_api_response(self, *args, **kwargs):
        return getattr(self.api, self.method)(*args, **kwargs)

    def handle_error_no_active_tokens(self, e, *args, **kwargs):
        if self.used_access_tokens and self.api:
            try:
                rate_limit_status = self.api.rate_limit_status()
            except self.error_class as e:
                if self.get_error_code(e) == 88:
                    self.used_access_tokens = []
                    return self.sleep_repeat_call(seconds=900, *args, **kwargs)
                raise

            method = '/%s' % self.method.replace('_', '/')
            status = [ methods for methods in rate_limit_status['resources'].values() if method in methods ][0][method]
            if status['remaining'] == 0:
                secs = (datetime.fromtimestamp(status['reset']) - datetime.now()).seconds
                self.used_access_tokens = []
                return self.sleep_repeat_call(seconds=secs, *args, **kwargs)
            return self.repeat_call(*args, **kwargs)
        else:
            return super(TwitterApi, self).handle_error_no_active_tokens(e, *args, **kwargs)

    def handle_error_code_88(self, e, *args, **kwargs):
        self.logger.warning('Rate limit exceeded: %s, method: %s recursion count: %d' % (
         e, self.method, self.recursion_count))
        token = AccessToken.objects.get_token_class(self.provider).delimeter.join([
         self.api.auth.access_token, self.api.auth.access_token_secret])
        self.used_access_tokens += [token]
        return self.repeat_call(*args, **kwargs)


def api_call(*args, **kwargs):
    api = TwitterApi()
    return api.call(*args, **kwargs)