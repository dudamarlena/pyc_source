# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestRedirect.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 879 bytes
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class RequestRedirect(AbstractRequest):
    opcode = 17

    def __init__(self, server, player):
        self.server = server
        self.player = player


class RequestRedirectCodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestRedirect)
        return varIntPrefixedStringEncoder(request.server) + varIntPrefixedStringEncoder(request.player)

    @staticmethod
    def decode(payload):
        server, payload = varIntPrefixedStringParser(payload)
        player, payload = varIntPrefixedStringParser(payload)
        return RequestRedirect(server, player)