# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/geobricks/geobricks/server/geobricks_common/geobricks_common/core/log.py
# Compiled at: 2015-06-04 04:13:35
import logging
from geobricks_common.config.config import config
settings = {'logging': {'level': config['settings']['logging']['level'], 
               'format': '%(asctime)s | %(levelname)-8s | Line: %(lineno)-5d  | %(name)-20s | %(message)s', 
               'datefmt': '%d-%m-%Y | %H:%M:%s'}}
level = settings['logging']['level']
format = settings['logging']['format']
datefmt = settings['logging']['datefmt']
logging.basicConfig(level=level, format=format, datefmt=datefmt)

def logger(loggerName=None):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    return logger