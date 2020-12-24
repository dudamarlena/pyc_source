# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/core/log.py
# Compiled at: 2015-04-04 17:37:18
from __future__ import absolute_import, unicode_literals
import logging.config

def configure_logging(log_level, log_format, log_custom_format=None):
    log_custom_format = log_custom_format or log_format
    logging.config.dictConfig({b'version': 1, 
       b'disable_existing_loggers': True, 
       b'formatters': {b'quiet': {b'format': b'%(asctime)s [%(levelname)s] %(message)s'}, 
                       b'verbose': {b'format': b'PID%(process)d %(asctime)s [%(levelname)s:%(name)s:%(lineno)d] %(message)s'}, 
                       b'custom': {b'format': log_custom_format}}, 
       b'handlers': {b'console': {b'level': b'DEBUG', 
                                  b'class': b'logging.StreamHandler', 
                                  b'formatter': log_format}}, 
       b'loggers': {b'logdog': {b'handlers': [
                                            b'console'], 
                                b'level': log_level, 
                                b'propagate': False}, 
                    b'tornado': {b'handlers': [
                                             b'console'], 
                                 b'level': log_level, 
                                 b'propagate': False}, 
                    b'zmq': {b'handlers': [
                                         b'console'], 
                             b'level': log_level, 
                             b'propagate': False}}})