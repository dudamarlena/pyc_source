# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\exceptions.py
# Compiled at: 2020-04-19 22:19:19
# Size of source mod 2**32: 451 bytes
__doc__ = '\n    exceptions.py\n    ~~~~~~~~~~\n\n'

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