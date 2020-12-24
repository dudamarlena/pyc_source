# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/log.py
# Compiled at: 2019-12-11 03:09:48
import logging, sys
LOGGER = logging.getLogger('clocwalk')
try:
    from clocwalk.lib.ansistrm import ColorizingStreamHandler
    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S')
FORMATTER_DEV = logging.Formatter('[%(asctime)s] [%(pathname)s(%(lineno)d)%(funcName)s()] [%(levelname)s] %(message)s', '%H:%M:%S')
LOGGER_HANDLER.setFormatter(FORMATTER_DEV)
LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)