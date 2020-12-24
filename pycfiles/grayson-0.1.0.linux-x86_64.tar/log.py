# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/log.py
# Compiled at: 2012-05-04 08:30:23
""" system """
import logging, logging.handlers, os, sys

class LogManager:
    theInstance = None

    def __init__(self, logLevel='info', logDir=None, toFile=None):
        self.loggingLevel = logLevel
        if logDir:
            self.logDirectory = logDir
        else:
            self.logDirectory = 'logs'
        self.logLevels = {'debug': logging.DEBUG, 'info': logging.INFO, 
           'warning': logging.WARNING, 
           'error': logging.ERROR, 
           'critical': logging.CRITICAL}
        level = self.logLevels[self.loggingLevel]
        self.fileHandler = None
        handler = logging.StreamHandler(sys.stdout)
        if toFile:
            if not os.path.exists(self.logDirectory):
                os.makedirs(self.logDirectory)
            logFile = os.path.join(self.logDirectory, toFile)
            if os.path.exists(logFile):
                try:
                    os.remove(logFile)
                except OSError as e:
                    logging.error('unable to remove %s', logFile)

            handler = logging.handlers.RotatingFileHandler(logFile, maxBytes=10000000, backupCount=3)
            self.fileHandler = handler
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        return

    def getFileHandler(self):
        return self.fileHandler

    def setLogLevel(self, level):
        oldLevel = None
        if level:
            logger = logging.getLogger()
            oldLevel = self.loggingLevel
            self.loggingLevel = level
            logger.setLevel(self.logLevels[level])
            return oldLevel
        else:
            return

    @staticmethod
    def getInstance(logLevel=None, logDir=None, toFile=None):
        if not logLevel:
            logLevel = 'info'
        if not logDir:
            logDir = 'logs'
        if LogManager.theInstance == None:
            LogManager.theInstance = LogManager(logLevel, logDir, toFile)
        return LogManager.theInstance