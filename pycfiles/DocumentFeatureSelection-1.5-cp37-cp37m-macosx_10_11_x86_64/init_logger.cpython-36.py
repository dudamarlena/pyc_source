# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codes/DocumentFeatureSelection/init_logger.py
# Compiled at: 2018-10-24 07:51:15
# Size of source mod 2**32: 483 bytes
import logging, sys
from logging import Formatter, StreamHandler
custmoFormatter = Formatter(fmt='[%(asctime)s]%(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s',
  datefmt='Y/%m/%d %H:%M:%S')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(custmoFormatter)
LOGGER_NAME = 'DocumentFeatureSelection'
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False