# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/util/Logger.py
# Compiled at: 2019-10-17 11:13:04
# Size of source mod 2**32: 338 bytes
import logging

def get_logger(module):
    """

    :param module:
    :return:
    """
    logging.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S',
      level=(logging.DEBUG))
    return logging.getLogger(module if isinstance(module, str) else module.__class__.__name__)