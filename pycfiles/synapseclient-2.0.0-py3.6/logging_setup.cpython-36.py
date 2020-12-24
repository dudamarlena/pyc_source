# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/logging_setup.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 3035 bytes
import logging, logging.config as logging_config
logging.captureWarnings(True)
logging.getLogger('requests').setLevel(logging.WARNING)
DEBUG_LOGGER_NAME = 'synapseclient_debug'
DEFAULT_LOGGER_NAME = 'synapseclient_default'
SILENT_LOGGER_NAME = 'synapseclient_silent'

class LoggingInfoOnlyFilter(logging.Filter):

    def filter(self, record):
        return record.levelno == logging.INFO


class LoggingIgnoreInfoFilter(logging.Filter):

    def filter(self, record):
        return record.levelno != logging.INFO


logging_config.dictConfig({'version':1, 
 'disable_existing_loggers':False, 
 'formatters':{'debug_format':{'format': '%(asctime)s [%(module)s:%(lineno)d - %(levelname)s]: %(message)s'}, 
  'brief_format':{'format': '%(message)s'}, 
  'warning_format':{'format': '[%(levelname)s] %(message)s'}}, 
 'filters':{'info_only':{'()': LoggingInfoOnlyFilter}, 
  'ignore_info':{'()': LoggingIgnoreInfoFilter}}, 
 'handlers':{'info_only_stdout':{'level':'INFO', 
   'class':'logging.StreamHandler', 
   'formatter':'brief_format', 
   'stream':'ext://sys.stdout', 
   'filters':[
    'info_only']}, 
  'debug_stderr':{'level':'DEBUG', 
   'class':'logging.StreamHandler', 
   'formatter':'debug_format', 
   'stream':'ext://sys.stderr'}, 
  'warning_stderr':{'level':'WARNING', 
   'class':'logging.StreamHandler', 
   'formatter':'warning_format', 
   'stream':'ext://sys.stderr'}}, 
 'loggers':{DEFAULT_LOGGER_NAME: {'handlers':[
                         'info_only_stdout', 'warning_stderr'], 
                        'level':'INFO', 
                        'propagate':True}, 
  
  DEBUG_LOGGER_NAME: {'handlers':[
                       'info_only_stdout', 'debug_stderr'], 
                      'level':'DEBUG', 
                      'propagate':True}, 
  
  SILENT_LOGGER_NAME: {'handlers':[],  'level':'INFO', 
                       'propagate':False}}})