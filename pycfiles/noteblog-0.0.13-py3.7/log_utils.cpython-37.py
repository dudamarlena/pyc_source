# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/log_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 2264 bytes
"""
切记: 不要重复创造日志对象，否则会重复打印
"""
from logging import handlers, getLogger
from logging import Formatter as LoggingFormatter
from logging import StreamHandler as LoggingStreamHandler
from logging import FileHandler as LoggingFileHandler
from logging import ERROR as LOGGING_ERROR
from logging import DEBUG as LOGGING_DEBUG
__all__ = [
 'set_logger']
CONSOLE_FORMATTER = '%(asctime)s [%(levelname)-6s] ➞ %(message)s'
FILE_FORMATTER = '%(asctime)s [%(levelname)-6s] at %(filename)s 出错函数%(funcName)s.%(lineno)d ↴\n %(message)s\n'

def set_logger(log_file_name, console_log_level=LOGGING_DEBUG, file_log_level=LOGGING_ERROR, console_formatter=CONSOLE_FORMATTER, file_formatter=FILE_FORMATTER, logger_name='my_logger'):
    logger = getLogger(logger_name)
    logger.setLevel(LOGGING_DEBUG)
    file_handler = handlers.RotatingFileHandler(filename=log_file_name,
      maxBytes=1048576,
      backupCount=5,
      encoding='utf-8')
    file_handler.setLevel(file_log_level)
    console_handler = LoggingStreamHandler()
    console_handler.setLevel(console_log_level)
    _console_formatter = LoggingFormatter(console_formatter)
    _file_formatter = LoggingFormatter(file_formatter)
    console_handler.setFormatter(_console_formatter)
    file_handler.setFormatter(_file_formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger