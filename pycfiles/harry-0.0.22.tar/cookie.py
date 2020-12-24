# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/cookie.py
# Compiled at: 2012-06-19 11:02:04


class Cookie(object):

    def __init__(self, j):
        self.raw = j
        self.name = self.raw['name']
        self.value = self.raw['value']
        if 'path' in self.raw:
            self.path = self.raw['path']
        else:
            self.path = ''
        if 'domain' in self.raw:
            self.domain = self.raw['path']
        else:
            self.domain = ''
        if 'expires' in self.raw:
            self.expires = self.raw['expires']
        else:
            self.expires = ''
        if 'httpOnly' in self.raw:
            self.http_only = self.raw['httpOnly']
        else:
            self.http_only = ''
        if 'secure' in self.raw:
            self.secure = self.raw['secure']
        else:
            self.secure = ''
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''