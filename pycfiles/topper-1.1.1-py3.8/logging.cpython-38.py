# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topper/utils/logging.py
# Compiled at: 2020-05-05 04:56:07
# Size of source mod 2**32: 453 bytes
import logging

def get_logger(name):
    """
    Return a logger with the specified name, creating it if necessary.
    :param name: module name
    :return: logging.Logger
    """
    logging.basicConfig(level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
      datefmt='%Y-%m-%d_%H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger