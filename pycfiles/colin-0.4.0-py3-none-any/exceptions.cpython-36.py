# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/core/exceptions.py
# Compiled at: 2018-04-19 02:54:30
# Size of source mod 2**32: 879 bytes


class ColinException(Exception):
    __doc__ = ' Generic exception when something goes wrong with colin. '


class ColinRulesetException(Exception):
    __doc__ = ' Exception raise when there is a problem with ruleset files. '