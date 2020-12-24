# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/utils/logger.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 4940 bytes
import os, logging
from logging.handlers import RotatingFileHandler
from ComunioScore import ROOT_DIR

class Logger:
    __doc__ = "Singleton class Logger to set up a Logger instance\n    USAGE:\n            Logger(name='ComunioScore')\n    "
    _Logger__instance = None

    def __init__(self, name='CommunioScore', level='info', log_folder='/var/log/', log_max_bytes=10000000, backup=5):
        if Logger._Logger__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            Logger._Logger__instance = self
        if isinstance(name, str):
            self.logger_name = name
            self.logger = logging.getLogger(name)
        else:
            raise TypeError("'name' must be type of string")
        if level == 'info':
            self.level = logging.INFO
        else:
            if level == 'debug':
                self.level = logging.DEBUG
            else:
                if level == 'warn':
                    self.level = logging.WARN
                else:
                    if level == 'error':
                        self.level = logging.ERROR
                    else:
                        self.level = logging.INFO
                self.logger.setLevel(self.level)
                self.formatter = logging.Formatter('%(asctime)s - %(lineno)d@%(filename)s - %(levelname)s: %(message)s')
                self.local_log = ROOT_DIR + '/logs'
                if self._Logger__create_log_folder(log_folder):
                    info_log_file_path = log_folder + '/' + self.logger_name + '/info.log'
                    error_log_file_path = log_folder + '/' + self.logger_name + '/error.log'
                    self.set_up_handler(log_max_bytes, info_log_file_path, error_log_file_path, backup)
                else:
                    if self._Logger__create_log_folder(self.local_log):
                        info_log_file_path = self.local_log + '/' + self.logger_name + '/info.log'
                        error_log_file_path = self.local_log + '/' + self.logger_name + 'error.log'
                        self.set_up_handler(log_max_bytes, info_log_file_path, error_log_file_path, backup)
                    else:
                        print('could not create a logger instance')

    @staticmethod
    def get_instance():
        """ get logger instance

        :return: Logger: logger instance
        """
        if Logger._Logger__instance is None:
            Logger()
        return Logger._Logger__instance

    def __create_log_folder(self, log_folder):
        """creates log folder in '/var/log/bierschi/ComunioScoreApp'

        :return bool, True if log folder was successfully created
        """
        try:
            if log_folder.endswith('/'):
                if not os.path.exists(log_folder):
                    os.mkdir(log_folder)
                if not os.path.exists(log_folder + self.logger_name):
                    os.mkdir(log_folder + self.logger_name)
                    return True
                else:
                    return True
            else:
                if not os.path.exists(log_folder):
                    os.mkdir(log_folder)
                if not os.path.exists(log_folder + '/' + self.logger_name):
                    os.mkdir(log_folder + '/' + self.logger_name)
                    return True
                else:
                    return True
        except PermissionError as ex:
            print('Check permission for folder {}! Exception: {}'.format(log_folder, ex))
            return False

    def set_up_handler(self, log_file_size, info_log_file_path, error_log_file_path, backup):
        """ sets up the logger handler

        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(self.formatter)
        info_rotate_handler = RotatingFileHandler(info_log_file_path, mode='a', maxBytes=log_file_size, backupCount=backup)
        info_rotate_handler.setFormatter(self.formatter)
        info_rotate_handler.setLevel(logging.DEBUG)
        error_rotate_handler = RotatingFileHandler(error_log_file_path, mode='a', maxBytes=log_file_size, backupCount=backup)
        error_rotate_handler.setFormatter(self.formatter)
        error_rotate_handler.setLevel(logging.WARNING)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(info_rotate_handler)
        self.logger.addHandler(error_rotate_handler)

    def info(self, msg):
        """logs info messages

        :param msg: string messages
        """
        self.logger.info(msg)

    def debug(self, msg):
        """logs debug messages

        :param msg: string messages
        """
        self.logger.debug(msg)

    def warning(self, msg):
        """logs warning messages

        :param msg: string messages
        """
        self.logger.warning(msg)

    def error(self, msg):
        """logs error messages

        :param msg: string messages
        """
        self.logger.error(msg)


if __name__ == '__main__':
    logger = Logger()
    for i in range(0, 1000):
        logger.info('test_message')
        logger.error('test_error')