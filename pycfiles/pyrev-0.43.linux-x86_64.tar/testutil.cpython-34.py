# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/test/testutil.py
# Compiled at: 2017-02-20 22:22:31
# Size of source mod 2**32: 546 bytes
from logging import getLogger, DEBUG

def _enable_logger(logger):
    from logging import StreamHandler
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    return logger


def _disable_logger(logger):
    from logging import NullHandler
    logger.addHandler(NullHandler())
    return logger


def setup_logger(name, debug):
    logger = getLogger(name)
    if debug:
        return _enable_logger(logger)
    else:
        return _disable_logger(logger)