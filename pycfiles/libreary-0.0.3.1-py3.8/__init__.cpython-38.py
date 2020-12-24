# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/libreary/__init__.py
# Compiled at: 2020-03-19 14:48:15
# Size of source mod 2**32: 3453 bytes
import logging
from typing import Optional
from libreary.version import VERSION
from libreary.libreary import Libreary
from libreary.exceptions import *
from libreary.adapter_manager import AdapterManager
from libreary.ingester import Ingester
from libreary.scheduler import Scheduler
__author__ = 'Ben Glick'
__version__ = VERSION
AUTO_LOGNAME = -1

def set_stream_logger(name: str='libreary', level: int=logging.DEBUG, format_string: Optional[str]=None):
    """Add a stream log handler.
    Args:
         - name (string) : Set the logger name.
         - level (logging.LEVEL) : Set to logging.DEBUG by default.
         - format_string (string) : Set to None by default.
    Returns:
         - None
    """
    if format_string is None:
        format_string = '%(asctime)s %(name)s:%(lineno)d [%(levelname)s]  %(message)s'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    futures_logger = logging.getLogger('concurrent.futures')
    futures_logger.addHandler(handler)


def set_file_logger(filename: str, name: str='libreary', level: int=logging.DEBUG, format_string: Optional[str]=None):
    """Add a stream log handler.
    Args:
        - filename (string): Name of the file to write logs to
        - name (string): Logger name
        - level (logging.LEVEL): Set the logging level.
        - format_string (string): Set the format string
    Returns:
       -  None
    """
    if format_string is None:
        format_string = '%(asctime)s.%(msecs)03d %(name)s:%(lineno)d [%(levelname)s]  %(message)s'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    futures_logger = logging.getLogger('concurrent.futures')
    futures_logger.addHandler(handler)


class NullHandler(logging.Handler):
    __doc__ = 'Setup default logging to /dev/null since this is library.'

    def emit(self, record):
        pass


__all__ = [
 'Libreary', 'AdapterManager', 'Ingester', 'Scheduler', 'set_stream_logger',
 'set_file_logger', 'AUTO_LOGNAME']
logging.getLogger('libreary').addHandler(NullHandler())