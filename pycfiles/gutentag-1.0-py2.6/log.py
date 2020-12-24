# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\gutentag\log.py
# Compiled at: 2009-07-13 23:06:11
import logging
from django.conf import settings

def getlogger():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"', '%Y-%m-%d %a %H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return (logger, hdlr)


def debug(msg):
    (logger, hdlr) = getlogger()
    logger.debug(msg)
    logger.removeHandler(hdlr)