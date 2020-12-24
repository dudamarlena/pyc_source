# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/Exceptions.py
# Compiled at: 2018-02-17 18:43:51
# Size of source mod 2**32: 145 bytes


class ConnectedCarsException(Exception):

    def __init__(self, message, errors):
        super().__init__(errors)
        self.errors = errors