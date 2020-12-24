# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/prometeo/projects/ardy/ardy/utils/log.py
# Compiled at: 2018-03-24 11:47:25
# Size of source mod 2**32: 822 bytes
from __future__ import unicode_literals, print_function, absolute_import
import logging.config
LOGGING = {'version':1, 
 'disable_existing_loggers':False, 
 'formatters':{'console': {'format':'[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s', 
              'datefmt':'%H:%M:%S'}}, 
 'handlers':{'console': {'level':'DEBUG', 
              'class':'logging.StreamHandler', 
              'formatter':'console'}}, 
 'loggers':{'ardy': {'handlers':[
            'console'], 
           'level':'DEBUG', 
           'propagate':True}}}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('ardy')