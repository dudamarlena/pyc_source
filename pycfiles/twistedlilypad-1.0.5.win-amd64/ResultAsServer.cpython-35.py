# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Results\ResultAsServer.py
# Compiled at: 2015-01-14 16:07:39
# Size of source mod 2**32: 344 bytes
from AbstractResult import AbstractResult, AbstractResultCodec

class ResultAsServer(AbstractResult):
    opcode = 1

    def __init__(self):
        pass


class ResultAsServerCodec(AbstractResultCodec):

    @staticmethod
    def encode(packet):
        return ''

    @staticmethod
    def decode(payload):
        return ResultAsServer()