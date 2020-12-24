# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestAuthenticate.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 919 bytes
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class RequestAuthenticate(AbstractRequest):
    opcode = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password


class RequestAuthenticateCodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAuthenticate)
        return varIntPrefixedStringEncoder(request.username) + varIntPrefixedStringEncoder(request.password)

    @staticmethod
    def decode(payload):
        username, payload = varIntPrefixedStringParser(payload)
        password, payload = varIntPrefixedStringParser(payload)
        return RequestAuthenticate(username, password)