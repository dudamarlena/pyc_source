# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matthew/Documents/rets/env/lib/python3.8/site-packages/rets/exceptions.py
# Compiled at: 2020-03-03 14:04:26
# Size of source mod 2**32: 828 bytes


class RETSException(Exception):
    __doc__ = 'The RETS Server Returned an Issue'

    def __init__(self, reply_text=None, reply_code=None):
        self.reply_code = reply_code
        self.reply_text = reply_text

    def __repr__(self):
        return self.reply_text

    def __str__(self):
        return self.reply_text


class HTTPException(Exception):
    pass


class NotLoggedIn(Exception):
    __doc__ = 'Authentication Required to Access RETS server'


class ParseError(Exception):
    __doc__ = 'Could not successfully Parse the RETS Response'


class MissingVersion(Exception):
    __doc__ = 'The RETS Version is required'


class MaxrowException(Exception):
    __doc__ = 'The RETS Servers truncated the results with a <MAXROW/>'

    def __init__(self, rows_returned):
        self.rows_returned = rows_returned