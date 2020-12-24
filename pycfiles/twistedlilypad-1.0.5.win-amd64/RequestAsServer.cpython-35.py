# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestAsServer.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 876 bytes
from struct import unpack_from, pack
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class RequestAsServer(AbstractRequest):
    opcode = 1

    def __init__(self, address, port):
        self.address = address
        self.port = port


class RequestAsServerCodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAsServer)
        return varIntPrefixedStringEncoder(request.address) + pack('>H', request.port)

    @staticmethod
    def decode(payload):
        address, payload = varIntPrefixedStringParser(payload)
        port = unpack_from('>H', payload)
        return RequestAsServer(address, port)