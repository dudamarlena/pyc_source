# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pumblr/errors.py
# Compiled at: 2010-09-12 04:14:42


class PumblrError(Exception):
    """Pumblr exception"""

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class PumblrAuthError(PumblrError):
    """403 Forbidden exception"""


class PumblrRequestError(PumblrError):
    """400 Bad Request exception"""