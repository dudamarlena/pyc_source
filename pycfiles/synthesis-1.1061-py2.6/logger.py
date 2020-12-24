# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/logger.py
# Compiled at: 2011-01-11 00:48:50
import logging
from logging import config
from synthesis.borg import Borg
_defaultConfig = {}

class Logger(Borg):

    def __init__(self, configFile, loglevel=1):
        Borg.__init__(self)
        self.LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
           'warning': logging.WARNING, 
           'error': logging.ERROR, 
           'critical': logging.CRITICAL}
        try:
            config.fileConfig(configFile, _defaultConfig)
        except IOError:
            raise

        self.logger = logging.getLogger('synthesis.engine')
        self.logger.setLevel(loglevel)

    def getLogger(self, loggerName):
        return logging.getLogger(loggerName)

    def __quit__(self):
        print 'Shutting down logging system...'
        logging.shutdown()

    def log(self, message, loglevel=0):
        if loglevel == 0:
            self.logger.info(message)
        elif loglevel == 1:
            self.logger.debug(message)
        elif loglevel == 2:
            self.logger.warning(message)
        elif loglevel == 3:
            self.logger.error(message)
        elif loglevel == 4:
            self.logger.critical(message)