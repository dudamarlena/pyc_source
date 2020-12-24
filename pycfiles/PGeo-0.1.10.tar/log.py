# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/utils/log.py
# Compiled at: 2014-08-01 05:41:50
import logging
from pgeo.config.settings import settings
level = settings['logging']['level']
format = settings['logging']['format']
datefmt = settings['logging']['datefmt']
logging.basicConfig(level=level, format=format, datefmt=datefmt)

def logger(loggerName=None):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    return logger