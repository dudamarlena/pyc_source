# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/olxbr/BarterDude/barterdude/conf.py
# Compiled at: 2020-03-20 15:15:22
# Size of source mod 2**32: 275 bytes
import logging
from pythonjsonlogger import jsonlogger
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter('(levelname) (name) (pathname) (lineno)',
  timestamp=True))
logger = logging.getLogger('barterdude')
logger.addHandler(handler)