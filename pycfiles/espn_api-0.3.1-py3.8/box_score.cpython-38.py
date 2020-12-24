# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/box_score.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 1014 bytes
from .box_player import BoxPlayer

class BoxScore(object):
    __doc__ = ' '

    def __init__(self, data, pro_schedule, positional_rankings, week):
        self.home_team = data['home']['teamId']
        self.home_score = round(data['home']['rosterForCurrentScoringPeriod']['appliedStatTotal'], 2)
        home_roster = data['home']['rosterForCurrentScoringPeriod']['entries']
        self.home_lineup = [BoxPlayer(player, pro_schedule, positional_rankings, week) for player in home_roster]
        self.away_team = 0
        self.away_score = 0
        self.away_lineup = []
        if 'away' in data:
            self.away_team = data['away']['teamId']
            self.away_score = round(data['away']['rosterForCurrentScoringPeriod']['appliedStatTotal'], 2)
            away_roster = data['away']['rosterForCurrentScoringPeriod']['entries']
            self.away_lineup = [BoxPlayer(player, pro_schedule, positional_rankings, week) for player in away_roster]