# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/responses/base.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 582 bytes


class Response(object):
    headers = {'Content-Type': 'text/html'}

    def __init__(self, data=None, status=None, headers=None, exception=False, content_type=None):
        self.data = data
        self.status = status
        self.exception = exception
        self.content_type = content_type
        if headers:
            self.headers.update(headers)

    def header_items(self):
        if not self.headers:
            return []
        else:
            return self.headers.items()

    def render(self):
        if self.data is None:
            return bytes()
        else:
            return self.data