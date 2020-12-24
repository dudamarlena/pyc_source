# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/log.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 454 bytes
"""Additional logging methods."""
import logging, binascii

def log_binary(logger, message, **kwargs):
    """Log binary data if debug is enabled."""
    if logger.isEnabledFor(logging.DEBUG):
        output = ('{0}={1}'.format(k, binascii.hexlify(bytearray(v)).decode()) for k, v in sorted(kwargs.items()))
        logger.debug('%s (%s)', message, ', '.join(output))