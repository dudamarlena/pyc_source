# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jan/repos/warlock/warlock/exceptions.py
# Compiled at: 2019-05-15 14:13:57
""" List of errors used in warlock """

class InvalidOperation(RuntimeError):
    pass


class ValidationError(ValueError):
    pass