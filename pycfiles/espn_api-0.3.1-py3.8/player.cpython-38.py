# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/player.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 909 bytes
from .constant import POSITION_MAP, PRO_TEAM_MAP
from .utils import json_parsing

class Player(object):
    __doc__ = 'Player are part of team'

    def __init__(self, data):
        self.name = json_parsing(data, 'fullName')
        self.playerId = json_parsing(data, 'id')
        self.posRank = json_parsing(data, 'positionalRanking')
        self.eligibleSlots = [POSITION_MAP[pos] for pos in json_parsing(data, 'eligibleSlots')]
        self.acquisitionType = json_parsing(data, 'acquisitionType')
        self.proTeam = PRO_TEAM_MAP[json_parsing(data, 'proTeamId')]
        for pos in json_parsing(data, 'eligibleSlots'):
            if pos != 25:
                if '/' not in POSITION_MAP[pos] or '/' in self.name:
                    self.position = POSITION_MAP[pos]
                    break

    def __repr__(self):
        return 'Player(%s)' % (self.name,)