# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_vpp/protocols/utils.py
# Compiled at: 2017-06-08 10:01:53
# Size of source mod 2**32: 484 bytes
from typing import Union

def ones_complement_checksum(msg: Union[(bytes, bytearray)]):
    """
    Calculate the 16-bit one's complement of the one's complement sum of a message.

    :param msg: The message
    :return: The checksum
    """
    checksum = 0
    for i in range(0, len(msg), 2):
        current_word = (msg[i] << 8) + msg[(i + 1)]
        c = checksum + current_word
        checksum = (c & 65535) + (c >> 16)

    return ~checksum & 65535