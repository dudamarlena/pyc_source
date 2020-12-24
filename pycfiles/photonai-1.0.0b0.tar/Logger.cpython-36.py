# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/photonlogger/logger.py
# Compiled at: 2019-09-11 10:06:07
# Size of source mod 2**32: 5061 bytes
import datetime, inspect
from enum import Enum
from functools import total_ordering
from photonai.base.helper import Singleton

@Singleton
class Logger:

    def __init__(self):
        self.config = {'print_to_console':True, 
         'print_to_file':True}
        self.loggers = []
        self._log_level = self.LogLevel.INFO
        self.verbosity_level = 0
        self.log_level_console = self.LogLevel.INFO
        self.log_level_file = self.LogLevel.INFO
        self._print_to_console = self.config['print_to_console']

    @staticmethod
    def set_print_to_console(self, status: bool):
        self._print_to_console = status

    def set_log_level(self, level):
        """" Use this method to change the log level. """
        self._log_level = level

    def set_custom_log_file(self, logfile):
        self._logfile_name = logfile

    def set_verbosity(self, verbose=0):
        """ Use this method to change the log level from verbosity attribute of hyperpipe. """
        self.verbosity_level = verbose
        if verbose == 0:
            self.set_log_level(self.LogLevel.INFO)
        else:
            if verbose == 1:
                self.set_log_level(self.LogLevel.VERBOSE)
            else:
                if verbose == 2:
                    self.set_log_level(self.LogLevel.DEBUG)
                else:
                    self.set_log_level(self.LogLevel.WARN)

    def debug(self, message: str):
        if self._log_level <= self.LogLevel.DEBUG:
            self._distribute_log(message, 'DEBUG')

    def verbose(self, message: str):
        if self._log_level <= self.LogLevel.VERBOSE:
            self._distribute_log(message, 'VERBOSE')

    def info(self, message: str):
        if self._log_level <= self.LogLevel.INFO:
            self._distribute_log(message, 'INFO')

    def warn(self, message: str):
        if self._log_level <= self.LogLevel.WARN:
            self._distribute_log(message, 'WARN')

    def error(self, message: str):
        if self._log_level <= self.LogLevel.ERROR:
            self._distribute_log(message, 'ERROR')

    def _distribute_log(self, message: str, log_type: str):
        entry = self._generate_log_entry(message, log_type)
        if self._print_to_console:
            self._print_entry(entry)

    @staticmethod
    def _print_entry(entry: dict):
        date_str = entry['logged_date'].strftime('%Y-%m-%d %H:%M:%S')
        print('{0}'.format(entry['message']))

    @staticmethod
    def _generate_log_entry(message: str, log_type: str):
        """Todo: Get current user from user-service and add username to log_entry"""
        log_entry = {'log_type':log_type, 
         'logged_date':datetime.datetime.utcnow(), 
         'message':message}
        if inspect.stack()[3][3]:
            log_entry['called_by'] = inspect.stack()[3][3]
        else:
            log_entry['called_by'] = 'Unknown caller'
        return log_entry

    def store_logger_names(self, name):
        return self.loggers.append(name)

    @total_ordering
    class LogLevel(Enum):
        ERROR = 4
        WARN = 3
        INFO = 2
        VERBOSE = 1
        DEBUG = 0

        def __lt__(self, other):
            if self.__class__ is other.__class__:
                return self.value < other.value
            else:
                return NotImplemented


if __name__ == '__main__':
    logger = Logger()
    logger.set_verbosity(2)
    logger.debug('test-Log debug message')
    logger.info('test-Log info message')
    logger.warn('test-Log warn message')
    logger.error('test-Log error message')
    logger.set_verbosity(0)
    logger.debug('test-Log debug message')
    logger.info('test-Log info message')
    logger.warn('test-Log warn message')
    logger.error('test-Log error message')