# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-logmanager/flask_logmanager/models/loggers.py
# Compiled at: 2019-07-30 10:17:54
from flask_logmanager import loggerDict, loggingLevel
from .logger import Logger
from ..util import NotFoundLoggerError, NotAddLoggerError

class Loggers(list):
    """
    Loggers - manage list of logger
    """

    def __init__(self):
        list.__init__(self)
        for id in loggerDict:
            list.append(self, Logger(id=id))

    def append(self, el):
        raise NotAddLoggerError()

    def getLogger(self, id):
        for logger in self:
            if logger.id == id:
                return logger

        raise NotFoundLoggerError(id)