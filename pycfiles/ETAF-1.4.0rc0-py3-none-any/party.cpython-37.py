# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/base/utils/party.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 1361 bytes


class Party(object):
    __doc__ = '\n    Uniquely identify\n    '

    def __init__(self, role, party_id):
        self.role = role
        self.party_id = party_id

    def __hash__(self):
        return (
         self.role, self.party_id).__hash__()

    def __str__(self):
        return f"Party(role={self.role}, party_id={self.party_id})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return (
         self.role, self.party_id) < (other.role, other.party_id)

    def __eq__(self, other):
        return self.party_id == other.party_id and self.role == other.role

    def to_pb(self):
        from arch.api.proto import federation_pb2
        return federation_pb2.Party(partyId=(f"{self.party_id}"), name=(self.role))