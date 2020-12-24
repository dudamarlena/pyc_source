# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/engine/seats.py
# Compiled at: 2016-11-22 02:08:34
from pypokerengine.engine.pay_info import PayInfo
from pypokerengine.engine.player import Player

class Seats:

    def __init__(self):
        self.players = []

    def sitdown(self, player):
        self.players.append(player)

    def size(self):
        return len(self.players)

    def count_active_players(self):
        return len([ p for p in self.players if p.is_active() ])

    def count_ask_wait_players(self):
        return len([ p for p in self.players if p.is_waiting_ask() ])

    def serialize(self):
        return [ player.serialize() for player in self.players ]

    @classmethod
    def deserialize(self, serial):
        seats = self()
        seats.players = [ Player.deserialize(s) for s in serial ]
        return seats