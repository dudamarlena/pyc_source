# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/utils/logger.py
# Compiled at: 2019-11-08 04:26:21
"""
----------
Kipp Utils
----------

"""
from __future__ import unicode_literals
import sys, time, logging
LOGNAME = b'kipp'

def get_formatter():
    formatter = logging.Formatter(b'[%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(name)s] - %(message)s')
    formatter.converter = time.gmtime
    return formatter


def get_stream_handler():
    formatter = get_formatter()
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    return ch


def setup_logger(logname, debug=False):
    """Create logger with default formatter and stream of stdout

    Args:
        logname (str): the name of the logger
        debug (bool, default=False): whether set logging level to DEBUG
    """
    logger = logging.getLogger(logname)
    log_level = logging.DEBUG if debug else logging.INFO
    stream_handler = get_stream_handler()
    logging.getLogger(b'tornado').addHandler(stream_handler)
    logging.getLogger(b'tornado').setLevel(logging.ERROR)
    logging.getLogger(b'concurrent').addHandler(stream_handler)
    logging.getLogger(b'concurrent').setLevel(logging.ERROR)
    logger.setLevel(log_level)
    if not logger.handlers:
        logger.addHandler(stream_handler)
    return logger


_logger = {b'ins': setup_logger(logname=LOGNAME)}

def get_logger():
    """Get kipp internal logger"""
    return _logger[b'ins']


def get_wrap_handler(target_logger):

    class _WrapperHandler(logging.StreamHandler):

        def emit(self, record):
            formatter = logging.Formatter(b'[%(levelname)s:%(name)s] %(message)s')
            target_logger.log(record.levelno, formatter.format(record))

    return _WrapperHandler()


def set_logger(logger):
    """Replace kipp internal logger

    Since of only Utilities' logger can output to file,
    so you need to replace the kipp' internal logger with Utilities' logger
    to save your logs to file.

    Usage:
    ::
        set_logger(utilities_logger)
    """
    handler = get_wrap_handler(logger)
    get_logger().addHandler(handler)
    for dep_logger_name in ('tornado', 'concurrent'):
        logging.getLogger(dep_logger_name).addHandler(handler)