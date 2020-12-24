# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload_friendly/cookie.py
# Compiled at: 2016-03-08 11:30:38
from collections import OrderedDict
COOKIE_ATTRIBUTE_NAMES = [
 'expires',
 'max-age',
 'domain',
 'path',
 'comment',
 'version',
 'secure',
 'httponly']

class CookieDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(CookieDict, self).__init__(*args, **kwargs)

    def render_to_string(self):
        """Render to cookie strings.
        """
        values = ''
        for key, value in self.items():
            values += ('{}={};').format(key, value)

        return values

    def from_cookie_string(self, cookie_string):
        """update self with cookie_string.
        """
        for key_value in cookie_string.split(';'):
            if '=' in key_value:
                key, value = key_value.split('=', 1)
            else:
                key = key_value
            strip_key = key.strip()
            if strip_key and strip_key.lower() not in COOKIE_ATTRIBUTE_NAMES:
                self[strip_key] = value.strip()