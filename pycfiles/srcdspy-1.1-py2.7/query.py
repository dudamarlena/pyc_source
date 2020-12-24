# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/srcdspy/query.py
# Compiled at: 2012-12-28 01:47:36
import socket
from srcdspy.util import *
PACKETSIZE = 1400
WHOLE = -1
SPLIT = -2
CHALLENGE = -1
S2C_CHALLENGE = 'A'
A2S_INFO = 'T'
A2S_INFO_STRING = 'Source Engine Query'
A2S_INFO_RESP = 'I'
A2S_PLAYER = 'U'
A2S_PLAYER_RESP = 'D'
A2S_RULES = 'V'
A2S_RULES_RESP = 'E'

def get_challenge(data):
    typ, data = unpack_byte(data)
    if typ == ord(S2C_CHALLENGE):
        return unpack_long(data)[0]


class QueryException(Exception):
    pass


class SourceQuery(object):

    def __init__(self):
        self.udpsock = None
        return

    def connect(self, address):
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.connect(address)

    def close(self):
        self.udpsock.close()

    def _receive(self):
        raw = self.udpsock.recv(PACKETSIZE)
        typ, raw = unpack_long(raw)
        if typ == WHOLE:
            return raw
        else:
            if typ == SPLIT:
                resp_id, raw = unpack_long(raw)
                total, raw = unpack_byte(raw)
                num, raw = unpack_byte(raw)
                splitsize, raw = unpack_short(raw)
                result = [None] * total
                result[num] = raw
                while not all(result):
                    raw = self.udpsock.recv(PACKETSIZE)
                    inner_typ, raw = unpack_long(raw)
                    inner_resp_id, raw = unpack_long(raw)
                    if inner_typ == SPLIT and inner_resp_id == resp_id:
                        total, raw = unpack_byte(raw)
                        num, raw = unpack_byte(raw)
                        splitsize, raw = unpack_byte(raw)
                        result[num] = raw
                    else:
                        raise QueryException

                combined = ('').join(result)
                typ, combined = unpack_long(combined)
                if typ == WHOLE:
                    return combined
                raise SourceException
            return

    def info(self):
        self.udpsock.send(pack_long(WHOLE) + A2S_INFO + pack_string(A2S_INFO_STRING))
        raw = self._receive()
        typ, raw = unpack_byte(raw)
        if typ == ord(A2S_INFO_RESP):
            result = {}
            result['network_version'], raw = unpack_byte(raw)
            result['hostname'], raw = unpack_string(raw)
            result['map'], raw = unpack_string(raw)
            result['gamedir'], raw = unpack_string(raw)
            result['gamedesc'], raw = unpack_string(raw)
            result['appid'], raw = unpack_short(raw)
            result['numplayers'], raw = unpack_byte(raw)
            result['maxplayers'], raw = unpack_byte(raw)
            result['numbots'], raw = unpack_byte(raw)
            result['dedicated'], raw = unpack_byte(raw)
            result['os'], raw = unpack_byte(raw)
            result['passworded'], raw = unpack_byte(raw)
            result['secure'], raw = unpack_byte(raw)
            result['version'], raw = unpack_string(raw)
            try:
                edf, raw = unpack_byte(raw)
                result['edf'] = edf
                if edf & 128:
                    result['port'], raw = unpack_short(raw)
                if edf & 16:
                    result['steamid'], raw = unpack_longlong(raw)
                if edf & 64:
                    result['specport'], raw = unpack_short(raw)
                    result['specname'], raw = unpack_string(raw)
                if edf & 32:
                    result['tag'], raw = unpack_string(raw)
            except:
                pass

            return result
        raise QueryException

    def player(self):
        self.udpsock.send(pack_long(WHOLE) + A2S_PLAYER + pack_long(CHALLENGE))
        raw = self._receive()
        challenge = get_challenge(raw)
        self.udpsock.send(pack_long(WHOLE) + A2S_PLAYER + pack_long(challenge))
        raw = self._receive()
        typ, raw = unpack_byte(raw)
        if typ == ord(A2S_PLAYER_RESP):
            num_players, raw = unpack_byte(raw)
            result = []
            try:
                for i in xrange(num_players):
                    player = {}
                    player['index'], raw = unpack_byte(raw)
                    player['name'], raw = unpack_string(raw)
                    player['kills'], raw = unpack_long(raw)
                    player['time'], raw = unpack_float(raw)
                    result.append(player)

            except:
                pass

            return result
        raise QueryException

    def rules(self):
        self.udpsock.send(pack_long(WHOLE) + A2S_RULES + pack_long(CHALLENGE))
        raw = self._receive()
        challenge = get_challenge(raw)
        self.udpsock.send(pack_long(WHOLE) + A2S_RULES + pack_long(challenge))
        raw = self._receive()
        typ, raw = unpack_byte(raw)
        if typ != ord(A2S_RULES):
            rules = {}
            numrules, raw = unpack_short(raw)
            while len(raw) > 0:
                try:
                    key, raw = unpack_string(raw)
                    rules[key], raw = unpack_string(raw)
                except:
                    pass

            return rules
        raise QueryException