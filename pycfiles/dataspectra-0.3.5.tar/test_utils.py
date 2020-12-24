# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/folders/48/sszjkycn30lfqfm8tpwj16th0000gp/T/tmpbU5Jbn/lib/python/cloudstorage/test_utils.py
# Compiled at: 2017-06-05 14:28:18
"""Utils for testing."""

class MockUrlFetchResult(object):

    def __init__(self, status, headers, body):
        self.status_code = status
        self.headers = headers
        self.content = body
        self.content_was_truncated = False
        self.final_url = None
        return