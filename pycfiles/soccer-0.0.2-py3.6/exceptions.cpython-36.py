# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\exceptions.py
# Compiled at: 2018-02-26 13:10:53
# Size of source mod 2**32: 857 bytes
""" This module contains the exceptions for the soccer module """

class NoDataConnectorException(Exception):
    __doc__ = 'Raise when there is no data connector for the given season'

    def __init__(self, message, season, *args):
        self.message = message
        (super(NoDataConnectorException, self).__init__)(message, season, *args)


class SoccerDBNotFoundException(Exception):
    __doc__ = 'Raise when the soccer database could not be found '

    def __init__(self, message, *args):
        self.message = message
        (super(SoccerDBNotFoundException, self).__init__)(message, *args)


class InvalidTimeFrameException(Exception):
    __doc__ = 'Raise when an invalid timeframe object was passed '

    def __init__(self, message, timeframe, *args):
        self.message = message
        (super(InvalidTimeFrameException, self).__init__)(message, timeframe, *args)