# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/django_rlog/logger.py
# Compiled at: 2016-08-23 01:20:06
import logging, logging.handlers
from django_rlog.defaults import DEFAULT_BACKUP_COUNT, DEFAULT_FILENAME, DEFAULT_HANDLER, DEFAULT_MAX_BYTES, DEFAULT_WHEN

def get_handler(**options):
    """Support FileHandler/RotatingFileHandler/TimedRotatingFileHandler"""
    filename = options.get('filename', DEFAULT_FILENAME)
    handler = options.get('handler', DEFAULT_HANDLER)
    when = options.get('when', DEFAULT_WHEN)
    maxBytes = options.get('maxBytes', DEFAULT_MAX_BYTES)
    backupCount = options.get('backupCount', DEFAULT_BACKUP_COUNT)
    if handler == 'TimedRotatingFileHandler':
        return logging.handlers.TimedRotatingFileHandler(filename, when=when, backupCount=backupCount)
    else:
        if handler == 'RotatingFileHandler':
            return logging.handlers.RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
        return logging.FileHandler(filename)


def get_logger(**options):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_handler(**options))
    return logger