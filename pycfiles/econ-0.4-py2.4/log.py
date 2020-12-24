# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/log.py
# Compiled at: 2007-04-18 06:57:54
"""
Econ logger
"""
import logging, logging.handlers, os, econ
logging_level = econ.conf.get('logging', 'level')
logging_log_file_path = econ.conf.get('logging', 'log_file_path')
application_name = 'econ'

def get_logger():
    """
    Convenience method to get instance of a python logger named after the
    application
    """
    return logging.getLogger(application_name)


def init_logging():
    """
    Configure the logger system in code.
    Two loggers: root + application
    Two output sources: file + stderr
    Only log level at ERROR or above go to stderr
    Log level for output to file is configurable via logging.level
    """
    logLevel = None
    logLevels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}
    if logging_level in logLevels:
        logLevel = logLevels[logging_level]
    else:
        raise 'Logging level not in valid list: %s' % (' ').join(logLevels.keys())
    consoleFormat = '%(name)s [%(levelname)s] %(message)s'
    consoleFormatter = logging.Formatter(consoleFormat)
    fileFormat = '[%(asctime)s] %(message)s'
    fileFormatter = logging.Formatter(fileFormat)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.ERROR)
    fileHandler = logging.handlers.RotatingFileHandler(logging_log_file_path, mode='a+', maxBytes=10000000, backupCount=5)
    consoleHandler.setFormatter(consoleFormatter)
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logLevel)
    rootLogger = logging.getLogger('')
    applicationLogger = logging.getLogger(application_name)
    rootLogger.addHandler(consoleHandler)
    applicationLogger.addHandler(fileHandler)
    applicationLogger.setLevel(logLevel)
    return


init_logging()
log = get_logger()
log.warning('Logging initialised.')