# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/box_player.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 1840 bytes
from .constant import POSITION_MAP, PRO_TEAM_MAP
from .player import Player
from datetime import datetime, timedelta

class BoxPlayer(Player):
    __doc__ = 'player with extra data from a matchup'

    def __init__(self, data, pro_schedule, positional_rankings, week):
        super(BoxPlayer, self).__init__(data)
        self.slot_position = 'FA'
        self.points = 0
        self.projected_points = 0
        self.pro_opponent = 'None'
        self.pro_pos_rank = 0
        self.game_played = 100
        if 'lineupSlotId' in data:
            self.slot_position = POSITION_MAP[data['lineupSlotId']]
        player = data['playerPoolEntry']['player'] if 'playerPoolEntry' in data else data['player']
        if player['proTeamId'] in pro_schedule:
            opp_id, date = pro_schedule[player['proTeamId']]
            self.game_played = 100 if datetime.now() > datetime.fromtimestamp(date / 1000.0) + timedelta(hours=3) else 0
            if str(player['defaultPositionId']) in positional_rankings:
                self.pro_opponent = PRO_TEAM_MAP[opp_id]
                self.pro_pos_rank = positional_rankings[str(player['defaultPositionId'])][str(opp_id)]
        player_stats = player['stats']
        for stats in player_stats:
            if stats['statSourceId'] == 0 and stats['scoringPeriodId'] == week:
                self.points = round(stats['appliedTotal'], 2)
            elif stats['statSourceId'] == 1 and stats['scoringPeriodId'] == week:
                self.projected_points = round(stats['appliedTotal'], 2)

    def __repr__(self):
        return 'Player(%s, points:%d, projected:%d)' % (self.name, self.points, self.projected_points)