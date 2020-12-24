# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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