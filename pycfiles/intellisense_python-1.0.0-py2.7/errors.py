# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellisense/errors.py
# Compiled at: 2013-10-08 10:43:23


class ApiError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return repr(self.message)