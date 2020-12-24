# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\baker\logger.py
# Compiled at: 2018-05-21 11:17:45
# Size of source mod 2**32: 677 bytes
import sys, logging
from baker import settings

def init():
    """
    Initialize logger for all application
    """
    global LOGGER
    LOGGER = logging.getLogger()
    level = 'DEBUG' if settings.get('DEBUG') else 'INFO'
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)


def log(*args):
    """
    Logging usual message on cli
    """
    globals()['LOGGER'].info(' '.join(args))


def debug(*args):
    """
    Logging debug information on cli
    """
    globals()['LOGGER'].debug('DEBUG: ' + ' '.join(args))