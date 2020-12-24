# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2players\playerPreGame.py
# Compiled at: 2018-07-17 08:18:18
# Size of source mod 2**32: 2389 bytes
"""
convert PlayerRecord data into PlayerPreGame
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sc2players.playerRecord import PlayerRecord
from sc2players import constants as c

class PlayerPreGame(PlayerRecord):

    def __init__(self, playerProfile, selectedRace=c.RANDOM, observe=False, playerID=0):
        if isinstance(playerProfile, PlayerPreGame):
            self.selectedRace = playerProfile.selectedRace
            self.isObserver = playerProfile.isObserver
            self.playerID = playerProfile.playerID
        else:
            self.selectedRace = c.SelectRaces(selectedRace)
            self.isObserver = observe
            self.playerID = playerID
        super(PlayerPreGame, self).__init__(source=playerProfile)

    def __repr__(self):
        added = ''
        if not self.isObserver:
            if self.playerID:
                added += '#%d ' % self.playerID
            added += '%s ' % self.race.type
        return '<%s %s%s %s-%s>' % (self.__class__.__name__,
         added, self.control.type, self.type.type, self.name)

    @property
    def control(self):
        """the type of control this player exhibits"""
        if self.isComputer:
            value = c.COMPUTER
        else:
            if self.isObserver:
                value = c.OBSERVER
            else:
                value = c.PARTICIPANT
        return c.PlayerControls(value)

    @property
    def race(self):
        """implemented to allow derived classes to define race identification differently"""
        return self.selectedRace