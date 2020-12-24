# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/utils/exceptions.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 256 bytes


class InputError(Exception):
    __doc__ = '\n    '

    def __init__(self, message):
        super(InputError, self).__init__(message)


class PlotError(Exception):
    __doc__ = '\n    '

    def __init__(self, message):
        super(PlotError, self).__init__(message)