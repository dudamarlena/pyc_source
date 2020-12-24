# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wavescli/logger.py
# Compiled at: 2020-04-24 09:34:39
# Size of source mod 2**32: 937 bytes
import logging
WAVES_LOGGER_CONFIG = {'version':1, 
 'handlers':{'default':{'level':logging.INFO, 
   'formatter':'standard', 
   'class':'logging.StreamHandler'}, 
  'waves':{'level':logging.INFO, 
   'formatter':'waves', 
   'class':'logging.StreamHandler'}}, 
 'formatters':{'standard':{'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}, 
  'waves':{'format': '%(asctime)s [%(levelname)s] %(name)s: [execution:%(execution)s] [task:%(task)s] %(message)s'}}, 
 'loggers':{'':{'handlers':[
    'default'], 
   'level':logging.INFO, 
   'propagate':True}, 
  'waves':{'handlers':[
    'waves'], 
   'level':logging.INFO, 
   'propagate':False}}}