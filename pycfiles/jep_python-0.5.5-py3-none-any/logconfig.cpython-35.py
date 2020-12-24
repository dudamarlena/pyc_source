# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\logconfig.py
# Compiled at: 2015-04-05 11:56:50
# Size of source mod 2**32: 843 bytes
import logging.config, sys
__author__ = 'mpagel'

def configure_test_logger():
    logging.config.dictConfig({'version': 1, 
     'disable_existing_loggers': False, 
     'formatters': {'simple': {'format': '%(asctime)s %(name)s %(levelname)s: %(message)s'}}, 
     
     'handlers': {'console': {'stream': sys.stdout, 
                              'class': 'logging.StreamHandler', 
                              'formatter': 'simple'}}, 
     
     'loggers': {'jep': {'handlers': ['console'], 
                         'propagate': False, 
                         'level': 'DEBUG'}}, 
     
     'root': {'level': 'WARNING', 
              'handlers': ['console']}})