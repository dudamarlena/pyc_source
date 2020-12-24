# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/utils/logger.py
# Compiled at: 2020-03-15 07:52:05
# Size of source mod 2**32: 5451 bytes
import os, time, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from credstuffer import ROOT_DIR

class Logger:
    """Logger"""
    _Logger__instance = None

    def __init__(self, account='', name='credstuffer', level='info', log_folder='/var/log/', log_max_bytes=10000000, backup=5):
        if Logger._Logger__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            Logger._Logger__instance = self
        if isinstance(name, str):
            self.logger_name = name
            self.logger = logging.getLogger(name)
        else:
            raise TypeError("'name' must be type of string")
        self.account_name = account
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
                datetime_obj = datetime.fromtimestamp(time.time())
                date_str = str(datetime_obj.date())
                time_str = str(datetime_obj.time()).split('.')[0]
                if self._Logger__create_log_folder(log_folder):
                    info_log_file_path = log_folder + '/' + self.logger_name + '/info_' + self.account_name + '_' + date_str + '_' + time_str + '_' + '.log'
                    error_log_file_path = log_folder + '/' + self.logger_name + '/error_' + self.account_name + '_' + date_str + '_' + time_str + '_' + '.log'
                    self.set_up_handler(log_max_bytes, info_log_file_path, error_log_file_path, backup)
                else:
                    if self._Logger__create_log_folder(self.local_log):
                        info_log_file_path = self.local_log + '/' + self.logger_name + '/info_' + self.account_name + '_' + date_str + '_' + time_str + '_' + '.log'
                        error_log_file_path = self.local_log + '/' + self.logger_name + '/error_' + self.account_name + '_' + date_str + '_' + time_str + '_' + '.log'
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
        """creates log folder in '/var/log/credstuffer'

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