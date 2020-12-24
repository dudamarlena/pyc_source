# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/conf/logger.py
# Compiled at: 2016-03-22 15:09:41
import os
from settings import *
__author__ = 'yanivshalev'
LOGGER_CONFIG = {'version': 1, 
   'disable_existing_loggers': False, 
   'formatters': {'simple': {'format': '%(name)s|%(asctime)s|%(levelname)s|%(module)s|%(funcName)s[%(lineno)d]|%(process)d|%(thread)d|%(message)s'}}, 
   'handlers': {'console': {'class': 'logging.StreamHandler', 
                            'level': 'DEBUG', 
                            'formatter': 'simple'}, 
                'info_file_handler': {'class': 'logging.handlers.RotatingFileHandler', 
                                      'level': 'INFO', 
                                      'formatter': 'simple', 
                                      'filename': os.path.join(LOG_DIR, 'info.log'), 
                                      'maxBytes': 10485760, 
                                      'backupCount': 20, 
                                      'encoding': 'utf8'}, 
                'error_file_handler': {'class': 'logging.handlers.RotatingFileHandler', 
                                       'level': 'ERROR', 
                                       'formatter': 'simple', 
                                       'filename': os.path.join(ERROR_DIR, 'errors.log'), 
                                       'maxBytes': 10485760, 
                                       'backupCount': 20, 
                                       'encoding': 'utf8'}}, 
   'loggers': {'my_module': {'level': 'ERROR', 
                             'handlers': [
                                        'console'], 
                             'propagate': 'no'}}, 
   'root': {'level': 'DEBUG', 
            'handlers': [
                       'console', 'info_file_handler', 'error_file_handler']}}