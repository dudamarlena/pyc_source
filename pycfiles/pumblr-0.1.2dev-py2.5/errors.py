# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    pass


class PumblrRequestError(PumblrError):
    """400 Bad Request exception"""
    pass