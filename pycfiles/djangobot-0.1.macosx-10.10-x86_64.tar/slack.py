# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scott/.envs/home/lib/python2.7/site-packages/djangobot/slack.py
# Compiled at: 2016-04-09 16:34:55
import logging, os, requests
logger = logging.getLogger('slackapi')

class SlackAPI(object):
    """
    Yet Another Slack Client
    """
    url = 'https://slack.com/api/{method}'

    def __init__(self, token=None, auth_test=False, verify=True, lazy=False):
        """
        Instantiation an instance of the Slack API

        Args:
            token: {str} (required) API token, read from SLACK_TOKEN env var
            auth_test: {bool} verify this token
            verify: {bool} verify all API calls return with a True 'ok'
            lazy: {bool} Don't populate properties until called
        """
        try:
            self.token = token if token else os.environ['SLACK_TOKEN']
        except KeyError:
            raise ValueError('If not providing a token, must set SLACK_TOKEN envvar')

        if auth_test:
            response = self.auth_test()
            if not response['ok']:
                raise ValueError(('Authentication Failed with response: {}').format(response))
        self.verify = verify
        self._channels = []
        self._users = []
        if not lazy:
            _ = self.channels
            _ = self.users

    def _call_api(self, method, params=None):
        """
        Low-level method to call the Slack API.

        Args:
            method: {str} method name to call
            params: {dict} GET parameters
                The token will always be added
        """
        url = self.url.format(method=method)
        if not params:
            params = {'token': self.token}
        else:
            params['token'] = self.token
        logger.debug('Send request to %s', url)
        response = requests.get(url, params=params).json()
        if self.verify:
            if not response['ok']:
                msg = 'For {url} API returned this bad response {response}'
                raise Exception(msg.format(url=url, response=response))
        return response

    @property
    def channels(self):
        """
        List of channels of this slack team
        """
        if not self._channels:
            self._channels = self._call_api('channels.list')['channels']
        return self._channels

    @property
    def users(self):
        """
        List of users of this slack team
        """
        if not self._users:
            self._users = self._call_api('users.list')['members']
        return self._users

    def auth_test(self):
        """
        Call auth.test
        """
        return self._call_api('auth.test')

    def rtm_start(self):
        """
        Call rtm.start
        """
        return self._call_api('rtm.start')

    def channel_from_name(self, name):
        """
        Return the channel dict given by human-readable {name}
        """
        try:
            channel = [ channel for channel in self.channels if channel['name'] == name
                      ][0]
        except IndexError:
            raise ValueError(('Unknown channel for name: "{}"').format(name))

        return channel

    def user_from_id(self, user_id):
        try:
            user = [ user for user in self.users if user['id'] == user_id
                   ][0]
        except IndexError:
            raise ValueError(('Unknown user for id: "{}"').format(user_id))

        return user

    def channel_from_id(self, channel_id):
        try:
            channel = [ channel for channel in self.channels if channel['id'] == channel_id
                      ][0]
        except IndexError:
            raise Exception(('Unkonwn channel for id: "{}"').format(channel_id))
        else:
            return channel