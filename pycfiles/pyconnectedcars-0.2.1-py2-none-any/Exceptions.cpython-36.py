# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/Exceptions.py
# Compiled at: 2018-02-17 18:43:51
# Size of source mod 2**32: 145 bytes


class ConnectedCarsException(Exception):

    def __init__(self, message, errors):
        super().__init__(errors)
        self.errors = errors