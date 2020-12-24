# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/logger.py
# Compiled at: 2020-04-18 16:07:01
# Size of source mod 2**32: 694 bytes
import logging, logging.handlers
FORMATTER = logging.Formatter('%(asctime)s [ %(levelname)s ] %(message)s')
LEVEL = logging.INFO
handler_file = logging.handlers.RotatingFileHandler('kutana.log',
  maxBytes=5243000, backupCount=5)
handler_file.setLevel(LEVEL)
handler_file.setFormatter(FORMATTER)
handler_stream = logging.StreamHandler()
handler_stream.setLevel(LEVEL)
handler_stream.setFormatter(FORMATTER)
logger = logging.getLogger('kutana')
logger.setLevel(LEVEL)
logger.addHandler(handler_stream)
logger.addHandler(handler_file)

def set_logger_level(level):
    handler_file.setLevel(level)
    handler_stream.setLevel(level)
    logger.setLevel(level)