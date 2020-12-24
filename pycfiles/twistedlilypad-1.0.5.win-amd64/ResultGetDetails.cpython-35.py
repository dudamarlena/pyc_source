# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Results\ResultGetDetails.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 1221 bytes
from struct import calcsize, unpack_from
from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class ResultGetDetails(AbstractResult):
    opcode = 34

    def __init__(self, ip, port, motd, version):
        self.ip = ip
        self.port = port
        self.motd = motd
        self.version = version


class ResultGetDetailsCodec(AbstractResultCodec):

    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetDetails)
        return varIntPrefixedStringEncoder(result.address) + pack('>H', result.port) + varIntPrefixedStringEncoder(result.motd) + varIntPrefixedStringEncoder(result.version)

    @staticmethod
    def decode(payload):
        ip, payload = varIntPrefixedStringParser(payload)
        port = unpack_from('>H', payload)
        payload = payload[calcsize('>H'):]
        motd, payload = varIntPrefixedStringParser(payload)
        version, payload = varIntPrefixedStringParser(payload)
        return ResultGetDetails(ip, port, motd, version)