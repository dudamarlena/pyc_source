# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utils/logger.py
# Compiled at: 2014-06-19 10:55:27
from protoLib.models import logEvent

class protoLog:

    def __init__(self, logUser, logTeam, logKey):
        self.logUser = logUser
        self.logTeam = logTeam
        self.logKey = logKey

    def info(self, logNotes='', logObject='', logInfo=''):
        self.logType = 'INF'
        logEvent(logObject, logInfo, self.logUser, self.logTeam, logNotes, self.logType, self.logKey)

    def error(self, logNotes='', logObject='', logInfo=''):
        self.logType = 'ERR'
        logEvent(logObject, logInfo, self.logUser, self.logTeam, logNotes, self.logType, self.logKey)