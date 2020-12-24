# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asistente04/diggi3/components/graph_db/graph_db/driver/orientdb/exceptions.py
# Compiled at: 2016-03-01 16:17:39
# Size of source mod 2**32: 966 bytes
from ... import types

class OrientDBException(types.GraphDBException):
    pass


class OrientDBConnectionError(types.GraphDBException):
    pass


class OrientDBQueryError(types.GraphDBException):

    def __init__(self, message, *args):
        exeptionPath = 'com.orientechnologies.orient.core.exception'
        start = message.find(exeptionPath)
        end = message.find('\n', start)
        FirstError = message[start + len(exeptionPath) + 1:end]
        FirstExceptionName, FirstExceptionDescription = FirstError.split(': ', 1)
        start = message.find(exeptionPath, end)
        end = message.find('\n', start)
        SecondError = message[start + len(exeptionPath) + 1:]
        SecondExceptionName, SecondExceptionDescription = SecondError.split(': ', 1)
        message = '%s: %s //// %s: %s' % (FirstExceptionName, FirstExceptionDescription, SecondExceptionName, SecondExceptionDescription)
        super(OrientDBQueryError, self).__init__(message, *args)