# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/response.py
# Compiled at: 2012-06-19 11:02:04
from . import cookie
from . import header
from . import content

class Response(object):

    def __init__(self, j):
        self.raw = j
        self.status = self.raw['status']
        self.status_text = self.raw['statusText']
        self.http_version = self.raw['httpVersion']
        self.cookies = []
        for c in self.raw['cookies']:
            self.cookies.append(cookie.Cookie(c))

        self.headers = []
        for c in self.raw['headers']:
            self.headers.append(header.Header(c))

        self.content = content.Content(self.raw['content'])
        if 'redirectUrl' in self.raw:
            self.redirect_url = self.raw['redirectUrl']
        else:
            self.redirect_url = ''
        self.headers_size = self.raw['headersSize']
        self.body_size = self.raw['bodySize']
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''