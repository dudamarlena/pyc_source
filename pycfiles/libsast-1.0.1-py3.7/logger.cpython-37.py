# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libsast/logger.py
# Compiled at: 2020-04-14 22:39:36
# Size of source mod 2**32: 462 bytes
"""Logger Config."""
import logging

def init_logger(module_name) -> logging.Logger:
    """Setup logger."""
    log_format = '[%(levelname)s] - %(asctime)-15s - %(name)s - %(message)s'
    logging.basicConfig(level=(logging.INFO),
      format=log_format,
      handlers=[
     logging.StreamHandler()])
    logger = logging.getLogger(module_name)
    return logger