# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/havenondemand/errorcodes.py
# Compiled at: 2016-10-21 10:54:21


class ErrorCode:
    TIMEOUT = 1600
    IN_PROGRESS = 1610
    QUEUED = 1620
    HTTP_ERROR = 1630
    CONNECTION_ERROR = 1640
    IO_ERROR = 1650
    INVALID_PARAM = 1660
    INVALID_HOD_RESPONSE = 1680


class HODErrorObject:
    error = 0
    reason = ''
    detail = ''
    jobID = ''


class HODErrors:
    errors = []

    def addError(self, error):
        self.errors.append(error)

    def resetErrorList(self):
        self.errors = []