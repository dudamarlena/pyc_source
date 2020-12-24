# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/websockets/websockets/utils.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 376 bytes
import itertools
__all__ = [
 'apply_mask']

def apply_mask(data: bytes, mask: bytes) -> bytes:
    """
    Apply masking to the data of a WebSocket message.

    :param data: Data to mask
    :param mask: 4-bytes mask

    """
    if len(mask) != 4:
        raise ValueError('mask must contain 4 bytes')
    return bytes((b ^ m for b, m in zip(data, itertools.cycle(mask))))