# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/transport/http.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 172 bytes


class HTTPTransport(object):

    def __init__(self, url, headers=None, cookies=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies