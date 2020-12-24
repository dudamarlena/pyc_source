# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dblapi\router.py
# Compiled at: 2018-03-18 13:07:26
# Size of source mod 2**32: 2627 bytes
from .errors import RequireFormatting

class Route(object):

    def __init__(self, url: str, method: str, require_format: bool=False):
        self.url = url
        self.method = method
        self.require_format = require_format

    def __str__(self) -> str:
        if self.require_format:
            raise RequireFormatting
        return self.url

    def __get__(self, instance, owner) -> str:
        if self.require_format:
            raise RequireFormatting
        return self.url

    def format_url(self, *args) -> str:
        return (self.url.format)(*args)


class Router(object):

    def __init__(self, base_url: str):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.base_bot = base_url + 'bots'
        self.base_usr = base_url + 'users/'
        self.base_wig = base_url + 'widget/'
        self.bot_search = Route(self.base_bot, 'GET')
        self.bot_get = Route(self.base_bot + '/{}', 'GET', True)
        self.bot_votes = Route(self.base_bot + '/{}/votes', 'GET', True)
        self.bot_stats = Route(self.base_bot + '/{}/stats', 'GET', True)
        self.bot_ul_stats = Route(self.base_bot + '{}/stats', 'POST', True)
        self.user_get = Route(self.base_usr + '{}', 'GET', True)
        self.widget_get = Route(self.base_wig + '{}.svg', 'GET', True)
        self.widget_owner = Route(self.base_wig + 'owner/{}.svg', 'GET', True)