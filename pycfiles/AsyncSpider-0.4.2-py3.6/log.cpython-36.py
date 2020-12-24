# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\core\log.py
# Compiled at: 2018-03-10 13:44:21
# Size of source mod 2**32: 700 bytes
import logging.config, sys
__all__ = [
 'logger']
logger = logging.getLogger('AsyncSpider')
logging.config.dictConfig(dict(version=1,
  loggers={'AsyncSpider': {'level':logging.INFO, 
                 'handlers':[
                  'console']}},
  handlers={'console': {'class':'logging.StreamHandler', 
             'formatter':'std', 
             'level':logging.INFO, 
             'stream':sys.__stdout__}},
  formatters={'std': {'format':'%(asctime)s [%(filename)s] [line:%(lineno)d] %(levelname)s: %(message)s', 
         'datefmt':'%Y:%m:%d %H:%M:%S'}}))