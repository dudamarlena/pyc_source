# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/core/http/exceptions.py
# Compiled at: 2019-05-11 03:13:00
# Size of source mod 2**32: 247 bytes


class HttpParseException(Exception):

    def __init__(self, msg, code=500):
        super(HttpParseException, self).__init__(msg)
        self.msg = msg
        self.code = code