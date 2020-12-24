# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roel.vandenberg/dev/lizard-connector/lizard_connector/exceptions.py
# Compiled at: 2018-03-13 11:03:24
# Size of source mod 2**32: 208 bytes


class LizardApiTooManyResults(Exception):
    pass


class LizardApiAsyncTaskFailure(Exception):
    pass


class InvalidUrlError(Exception):
    pass


class LizardApiImproperQueryError(Exception):
    pass