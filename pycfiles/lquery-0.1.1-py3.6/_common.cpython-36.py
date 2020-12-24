# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\extras\_common.py
# Compiled at: 2018-08-02 15:31:23
# Size of source mod 2**32: 272 bytes


class NotSupportError(Exception):
    pass


class AlwaysEmptyError(Exception):

    def __init__(self, reason: str):
        self.reason = reason