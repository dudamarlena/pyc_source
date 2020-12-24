# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/footylib/footylibExceptions.py
# Compiled at: 2018-01-13 12:10:33
# Size of source mod 2**32: 606 bytes


class MonthTranslationError(Exception):

    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return 'Cannot translate Dutch time to English for datetime object. {}'.format(self.error_msg)


class ErrorGettingDivision(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return "Specified division doesn't exist"


class ErrorGettingLeague(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return "Specified league doesn't exist"