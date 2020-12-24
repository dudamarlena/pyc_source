# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/artnet_message.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2381 bytes
import ctypes, functools
from . import log
DMX_LENGTH = 512
ARTNET_DMX = 20480
ARTNET_VERSION = 14
NAME = b'Art-Net\x00'
MAX_NET = 255
MAX_SUBNET = 15
MAX_UNIVERSE = 15
UDP_PORT = 6454

@functools.lru_cache(maxsize=DMX_LENGTH)
def MessageClass(length=DMX_LENGTH):
    if not 0 <= length <= DMX_LENGTH:
        raise AssertionError
    elif not length % 2 == 0:
        raise AssertionError('artnet only takes messages of even length')
    Char, Int8, Int16 = ctypes.c_char, ctypes.c_ubyte, ctypes.c_ushort

    class DMXMessage(ctypes.Structure):
        _fields_ = [
         (
          'id', Char * 8),
         (
          'opCode', Int16),
         (
          'protVerHi', Int8),
         (
          'protVerLo', Int8),
         (
          'sequence', Int8),
         (
          'physical', Int8),
         (
          'subUni', Int8),
         (
          'net', Int8),
         (
          'lengthHi', Int8),
         (
          'length', Int8),
         (
          'data', Int8 * length)]

    return DMXMessage


def dmx_message(length=None, net=0, subnet=0, universe=0, sequence=1, data=None):
    if length is None:
        length = DMX_LENGTH if data is None else len(data)
    else:
        if data is not None:
            assert len(data) == length
        else:
            Message = MessageClass(length)
            assert 0 <= sequence <= DMX_LENGTH
            assert 0 <= net <= MAX_NET
            assert 0 <= subnet <= MAX_SUBNET
            assert 0 <= universe <= MAX_UNIVERSE
        subUni = (subnet << 4) + universe
        hi, lo = divmod(length, 256)
        msg = Message(id=NAME,
          opCode=ARTNET_DMX,
          protVerLo=ARTNET_VERSION,
          sequence=sequence,
          net=net,
          subUni=subUni,
          lengthHi=hi,
          length=lo)
        if data is not None:
            msg.data[:] = data
    return msg


DMXMessage = MessageClass()
EMPTY_MESSAGE_SIZE = ctypes.sizeof(MessageClass(0))

def bytes_to_message(b):
    if not isinstance(b, bytearray):
        b = bytearray(b)
    else:
        length = len(b) - EMPTY_MESSAGE_SIZE
        assert 0 <= length <= DMX_LENGTH
        result = MessageClass(length).from_buffer(b)
        if result.id == NAME[:-1]:
            return result
    log.error('Expected name %s but got name %s', NAME[:-1], result.id)