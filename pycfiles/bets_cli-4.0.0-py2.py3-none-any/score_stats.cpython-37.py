# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\model\stats\score_stats.py
# Compiled at: 2019-05-15 19:14:11
# Size of source mod 2**32: 828 bytes
from bets.model.stats.outcome_stats import OutcomeStats

class ScoreStats(OutcomeStats):
    KEYS = OutcomeStats.KEYS + ['host_score', 'guest_score', 'goals_diff']
    host_score: int
    guest_score: int
    goals_diff: int

    def __init__(self, ratio_1, ratio_X, ratio_2, host_score, guest_score, host_team='', guest_team='', date='', country='', tournament=''):
        host_score = int(host_score)
        guest_score = int(guest_score)
        outcome = '1' if host_score > guest_score else '2' if guest_score > host_score else 'X'
        super().__init__(ratio_1, ratio_X, ratio_2, outcome, host_team, guest_team, date, country, tournament)
        self.host_score = host_score
        self.guest_score = guest_score
        self.goals_diff = abs(host_score - guest_score)