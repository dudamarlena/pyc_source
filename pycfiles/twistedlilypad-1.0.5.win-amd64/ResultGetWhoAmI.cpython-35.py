# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Results\ResultGetWhoAmI.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 695 bytes
from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class ResultGetWhoAmI(AbstractResult):
    opcode = 4

    def __init__(self, whoAmI):
        self.whoAmI = whoAmI


class ResultGetWhoAmICodec(AbstractResultCodec):

    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetWhoAmI)
        return varIntPrefixedStringEncoder(result.whoAmI)

    @staticmethod
    def decode(payload):
        whoAmI, payload = varIntPrefixedStringParser(payload)
        return ResultGetWhoAmI(whoAmI)