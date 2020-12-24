# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/log.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 454 bytes
__doc__ = 'Additional logging methods.'
import logging, binascii

def log_binary(logger, message, **kwargs):
    """Log binary data if debug is enabled."""
    if logger.isEnabledFor(logging.DEBUG):
        output = ('{0}={1}'.format(k, binascii.hexlify(bytearray(v)).decode()) for k, v in sorted(kwargs.items()))
        logger.debug('%s (%s)', message, ', '.join(output))