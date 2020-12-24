# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/entry.py
# Compiled at: 2012-06-19 11:02:04
from . import request
from . import response
from . import cache
from . import timings

class Entry(object):

    def __init__(self, j):
        self.raw = j
        if 'pageref' in self.raw:
            self.page_ref = self.raw['pageref']
        else:
            self.page_ref = ''
        self.started_date_time = self.raw['startedDateTime']
        self.time = self.raw['time']
        self.request = request.Request(self.raw['request'])
        self.response = response.Response(self.raw['response'])
        self.cache = cache.Cache(self.raw['cache'])
        if 'timings' in self.raw:
            self.timings = timings.Timings(self.raw['timings'])
        else:
            self.timings = timings.Timings({'send': None, 'wait': None, 'receive': None})
        if 'serverIPAddress' in self.raw:
            self.server_ip_address = self.raw['serverIPAddress']
        else:
            self.server_ip_address = ''
        if 'connection' in self.raw:
            self.connection = self.raw['connection']
        else:
            self.connection = ''
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''
        return