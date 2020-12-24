# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/diff_and_patch/exceptions.py
# Compiled at: 2018-08-26 08:43:52
# Size of source mod 2**32: 688 bytes


class InvalidDelta(ValueError):

    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors
        super(InvalidDelta, self).__init__(message=(self.message))


class NoDelta(InvalidDelta):

    def __init__(self, message=''):
        self.message = 'No difference detected {m}'.format(m=message)
        super(NoDelta, self).__init__(message=(self.message))


class PartialSuccess(Exception):

    def __init__(self, message, successes=None, errors=None):
        self.message = message
        self.successes = successes if successes else []
        self.errors = errors if errors else []
        super(PartialSuccess, self).__init__(message)