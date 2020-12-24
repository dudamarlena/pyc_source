# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_rest_engine/geobricks_rest_engine/core/log.py
# Compiled at: 2015-03-16 10:05:17
import logging
from geobricks_rest_engine.config.common_settings import settings
config = {'logging': {'level': settings['settings']['logging']['level'], 
               'format': '%(asctime)s | %(levelname)-8s | %(name)-20s | Line: %(lineno)-5d | %(message)s', 
               'datefmt': '%d-%m-%Y | %H:%M:%s'}}
level = config['logging']['level']
format = config['logging']['format']
datefmt = config['logging']['datefmt']
logging.basicConfig(level=level, format=format, datefmt=datefmt)

def logger(loggerName=None):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    return logger