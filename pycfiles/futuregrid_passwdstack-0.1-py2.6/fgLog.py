# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_passwdstack/utils/fgLog.py
# Compiled at: 2012-08-20 15:17:26
"""@package fgLog
Easy to use logging. Poll test
"""
import logging, logging.handlers, os

class fgLog:
    """ This class allows to conveniently create a logging file to which
    you can add warnings, errors, infos, and debug messages. For each type
    we provide a convenient method.
    """

    def __init__(self, logfile, loglevel, whois, verbose):
        """initializes the log file. the parameters are as follows

        @param logfile name of the log file

        @param loglevel setting of the log level. The log level has to
        be specified as an logging object. It can be logging.DEBUG, logging.ERROR, logging.INFO, logging.WARNING 

        @param whois name associated with the log

        @param verbose if True prints some information to stdout
 
       TODO: explain what the loglevels do
        """
        self._logfile = logfile
        self._logger = logging.getLogger(whois)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._logger.setLevel(loglevel)
        handler = logging.FileHandler(logfile)
        handler.setFormatter(self._formatter)
        handler.setLevel(loglevel)
        self._logger.addHandler(handler)
        self._logger.propagate = False
        if verbose:
            handler = logging.StreamHandler()
            handler.setLevel(loglevel)
            handler.setFormatter(self._formatter)
            self._logger.addHandler(handler)

    def getLogger(self, name):
        return logging.getLogger(name)

    def getLogFile(self):
        """returns the log file"""
        return self._logfile

    def debug(self, text):
        """includes a debug message of "text" into the log file.
        @param text the message written into the log file"""
        self._logger.debug(text)

    def info(self, text):
        """includes an info message of "text" into the log file
        @param text the message written into the log file"""
        self._logger.info(text)

    def warning(self, text):
        """includes a warning message of "text" into the log file
        @param text the message written into the log file"""
        self._logger.warning(text)

    def error(self, text):
        """includes an error message of "text" into the log file
        @param text the message written into the log file"""
        self._logger.error(text)

    def clear(self):
        """removes the log file"""
        os.remove(self._logfile)