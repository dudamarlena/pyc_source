# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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