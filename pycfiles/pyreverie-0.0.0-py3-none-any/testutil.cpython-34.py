# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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