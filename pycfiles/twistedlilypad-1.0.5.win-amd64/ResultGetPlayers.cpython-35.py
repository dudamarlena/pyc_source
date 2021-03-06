# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Results\ResultGetPlayers.py
# Compiled at: 2017-01-02 18:35:19
# Size of source mod 2**32: 2691 bytes
from struct import calcsize, unpack_from, pack
from uuid import UUID
from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringListEncoder

class ResultGetPlayers(AbstractResult):
    opcode = 32

    def __init__(self, listPlayers, currentPlayers, maxPlayers, players=None, includeUUIDs=None, uuids=None):
        self.listPlayers = listPlayers
        self.includeUUIDs = includeUUIDs
        self.currentPlayers = currentPlayers
        self.maxPlayers = maxPlayers
        self.players = players
        self.uuids = uuids
        if players is not None and uuids is not None:
            self.playersToUUID = dict(zip(players, uuids))
        else:
            self.playersToUUID = None


class ResultGetPlayersCodec(AbstractResultCodec):

    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetPlayers)
        ret = booleanEncoder(result.listPlayers) + pack('>HH', result.currentPlayers, result.maxPlayers)
        if result.listPlayers:
            return ret + varIntPrefixedStringListEncoder(result.players)
        if result.includeUUIDs is not None:
            ret += booleanEncoder(result.includeUUIDs)
            if result.includeUUIDs:
                for uuid in result.uuids:
                    ret += uuid.bytes

        return ret

    @staticmethod
    def decode(payload):
        listPlayers, currentPlayers, maxPlayers = unpack_from('>BHH', payload)
        listPlayers = listPlayers != 0
        payload = payload[calcsize('>BHH'):]
        if listPlayers:
            players = []
            for i in xrange(currentPlayers):
                player, payload = varIntPrefixedStringParser(payload)
                players.append(player)

            if not payload:
                return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players)

            def parse_uuid(payload):
                return (UUID(bytes=payload[:16]), payload[16:])

            includeUUIDs = unpack_from('>B', payload)[0] != 0
            payload = payload[calcsize('>B'):]
            if includeUUIDs:
                uuids = []
                for i in xrange(currentPlayers):
                    uuid, payload = parse_uuid(payload)
                    uuids.append(uuid)

                return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players, includeUUIDs, uuids)
            return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players, includeUUIDs)
        return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers)