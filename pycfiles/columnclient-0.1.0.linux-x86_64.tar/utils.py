# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/utils.py
# Compiled at: 2017-08-21 17:07:37


class MockResponse(object):
    """Mock class for requests.Response
    """

    def __init__(self, text='', status_code=200):
        self.text = text
        self.status_code = status_code

    def text(self):
        return self.text