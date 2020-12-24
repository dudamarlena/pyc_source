# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/utils/log.py
# Compiled at: 2018-03-24 11:47:25
from __future__ import unicode_literals, print_function, absolute_import
import logging.config
LOGGING = {b'version': 1, 
   b'disable_existing_loggers': False, 
   b'formatters': {b'console': {b'format': b'[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s', 
                                b'datefmt': b'%H:%M:%S'}}, 
   b'handlers': {b'console': {b'level': b'DEBUG', 
                              b'class': b'logging.StreamHandler', 
                              b'formatter': b'console'}}, 
   b'loggers': {b'ardy': {b'handlers': [
                                      b'console'], 
                          b'level': b'DEBUG', 
                          b'propagate': True}}}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(b'ardy')