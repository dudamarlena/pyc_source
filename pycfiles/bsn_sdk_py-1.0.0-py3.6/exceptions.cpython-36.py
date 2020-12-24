# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\exceptions.py
# Compiled at: 2020-04-19 22:19:19
# Size of source mod 2**32: 451 bytes
"""
    exceptions.py
    ~~~~~~~~~~

"""

class BsnException(Exception):

    def __init__(self, code, message):
        self._BsnException__code = code
        self._BsnException__message = message

    def to_unicode(self):
        return 'BsnException: code:{}, message:{}'.format(self._BsnException__code, self._BsnException__message)

    def __str__(self):
        return self.to_unicode()

    def __repr__(self):
        return self.to_unicode()


class BsnValidationError(Exception):
    pass