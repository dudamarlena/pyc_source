# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/log.py
# Compiled at: 2020-02-03 04:43:58
# Size of source mod 2**32: 671 bytes
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