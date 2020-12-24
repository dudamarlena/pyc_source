# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/conf.py
# Compiled at: 2020-04-30 17:51:17
# Size of source mod 2**32: 671 bytes
import logging, os
from pythonjsonlogger import jsonlogger
BARTERDUDE_DEFAULT_LOG_NAME = os.environ.get('BARTERDUDE_DEFAULT_LOG_NAME', 'barterdude')
BARTERDUDE_DEFAULT_LOG_LEVEL = int(os.environ.get('BARTERDUDE_DEFAULT_LOG_LEVEL', logging.INFO))
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('(levelname) (name) (pathname) (lineno)',
  timestamp=True))
default_logger = logging.getLogger(BARTERDUDE_DEFAULT_LOG_NAME)

def getLogger(name, level=BARTERDUDE_DEFAULT_LOG_LEVEL):
    logger = default_logger.getChild(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger