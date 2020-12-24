# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/codes/flexible_clustering_tree/flexible_clustering_tree/logger.py
# Compiled at: 2019-10-22 10:24:47
# Size of source mod 2**32: 525 bytes
from logging import getLogger, StreamHandler, FileHandler, Logger
import logging, sys
custmoFormatter = logging.Formatter(fmt='[%(asctime)s]%(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s',
  datefmt='Y/%m/%d %H:%M:%S')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(custmoFormatter)
logger_name = 'flexible-clustering-tree'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False