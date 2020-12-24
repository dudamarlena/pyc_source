# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_rest/errors.py
# Compiled at: 2013-03-18 20:58:20
from prism_core.errors import PrismError

class ViewModelNotFoundError(PrismError):
    pass


class AuthenticationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)