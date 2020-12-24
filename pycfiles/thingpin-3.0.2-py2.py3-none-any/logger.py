# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgk/projects/thingpin/src/thingpin/logger.py
# Compiled at: 2015-11-01 14:47:36
import logging, logging.handlers, sys

def Logger(name='thingpin', level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    if log_file is not None:
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10485760, backupCount=10)
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(process)d %(levelname)s %(message)s'))
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
    logger.addHandler(handler)
    return logger