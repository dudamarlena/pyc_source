# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\error.py
# Compiled at: 2015-01-11 13:52:03
import six

class ChatpyError(Exception):
    """Chatpy exception"""

    def __init__(self, reason, response=None):
        self.reason = six.text_type(reason)
        self.response = response
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason