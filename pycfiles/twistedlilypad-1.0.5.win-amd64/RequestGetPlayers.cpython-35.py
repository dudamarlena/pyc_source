# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Requests\RequestGetPlayers.py
# Compiled at: 2016-12-27 07:11:25
# Size of source mod 2**32: 1070 bytes
from struct import unpack_from, calcsize
from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder

class RequestGetPlayers(AbstractRequest):
    opcode = 32

    def __init__(self, listPlayers, includeUUIDs=False):
        self.listPlayers = listPlayers
        self.includeUUIDs = includeUUIDs


class RequestGetPlayersCodec(AbstractRequestCodec):

    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetPlayers)
        if request.includeUUIDs is None:
            return booleanEncoder(request.listPlayers)
        else:
            return booleanEncoder(request.listPlayers) + booleanEncoder(request.includeUUIDs)

    @staticmethod
    def decode(payload):
        listPlayers = unpack_from('>B', payload)[0] == 0
        if len(payload) > calcsize('>B'):
            includeUUIDs = unpack_from('>B', payload)[0] == 0
        else:
            includeUUIDs = False
        return RequestGetPlayers(listPlayers, includeUUIDs)