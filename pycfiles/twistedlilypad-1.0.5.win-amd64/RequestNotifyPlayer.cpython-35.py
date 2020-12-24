# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestNotifyPlayer.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 960 bytes
from struct import unpack_from, calcsize
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringListEncoder

class RequestNotifyPlayer(AbstractRequest):
    opcode = 33

    def __init__(self, add, player):
        self.add = add
        self.player = player


class RequestNotifyPlayerCodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestNotifyPlayer)
        return booleanEncoder(request.add) + varIntPrefixedStringListEncoder(request.player)

    @staticmethod
    def decode(payload):
        add = unpack_from('>B', payload) == 0
        payload = payload[calcsize('>B'):]
        player, payload = varIntPrefixedStringParser(payload)
        return RequestNotifyPlayer(add, player)