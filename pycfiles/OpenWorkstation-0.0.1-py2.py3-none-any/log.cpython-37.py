# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/util/log.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 1070 bytes
import logging
from logging.config import dictConfig
from workstation.util import environment
LOG_FILENAME = environment.get_path('LOG_FILE')
logging_config = dict(version=1,
  formatters={'basic': {'format': '%(asctime)s %(name)s %(levelname)s [Line %(lineno)s]     %(message)s'}},
  handlers={'debug':{'class':'logging.StreamHandler', 
  'formatter':'basic', 
  'level':logging.DEBUG}, 
 'development':{'class':'logging.StreamHandler', 
  'formatter':'basic', 
  'level':logging.WARNING}, 
 'file':{'class':'logging.handlers.RotatingFileHandler', 
  'formatter':'basic', 
  'filename':LOG_FILENAME, 
  'maxBytes':5000000, 
  'level':logging.INFO, 
  'backupCount':3}},
  root={'handlers':[
  'file'], 
 'level':logging.DEBUG})
dictConfig(logging_config)

def get_logger(name=None):
    return logging.getLogger(name)