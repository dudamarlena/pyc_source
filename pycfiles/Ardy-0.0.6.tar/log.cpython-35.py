# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/utils/log.py
# Compiled at: 2018-03-24 11:47:25
# Size of source mod 2**32: 822 bytes
from __future__ import unicode_literals, print_function, absolute_import
import logging.config
LOGGING = {'version': 1, 
 'disable_existing_loggers': False, 
 'formatters': {'console': {'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s', 
                            'datefmt': '%H:%M:%S'}}, 
 
 'handlers': {'console': {'level': 'DEBUG', 
                          'class': 'logging.StreamHandler', 
                          'formatter': 'console'}}, 
 
 'loggers': {'ardy': {'handlers': ['console'], 
                      'level': 'DEBUG', 
                      'propagate': True}}}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('ardy')