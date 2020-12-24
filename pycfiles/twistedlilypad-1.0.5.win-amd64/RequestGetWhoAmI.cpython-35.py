# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestGetWhoAmI.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 434 bytes
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec

class RequestGetWhoAmI(AbstractRequest):
    opcode = 4

    def __init__(self):
        pass


class RequestGetWhoAmICodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetWhoAmI)
        return ''

    @staticmethod
    def decode(payload):
        return RequestGetWhoAmI()