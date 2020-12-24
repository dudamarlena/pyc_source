# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/constants.py
# Compiled at: 2015-07-09 21:30:20
# Size of source mod 2**32: 579 bytes
import os, logging, pynhost
DEFAULT_LOGGING_DIRECTORY = os.path.join(os.path.dirname(pynhost.__file__), 'logs')
DEFAULT_INPUT_SOURCE = os.path.join(os.path.dirname(os.path.abspath(pynhost.__file__)), 'pynportal')
LOGGING_LEVELS = {'off': logging.NOTSET, 
 'notset': logging.NOTSET, 
 'debug': logging.DEBUG, 
 'on': logging.INFO, 
 'info': logging.INFO, 
 'warning': logging.WARNING, 
 'error': logging.ERROR, 
 'critical': logging.CRITICAL}
MAX_HISTORY_LENGTH = 101
MAIN_LOOP_DELAY = 0.1
DEFAULT_DEBUG_DELAY = 4
DEFAULT_PORT_NUMBER = 10001