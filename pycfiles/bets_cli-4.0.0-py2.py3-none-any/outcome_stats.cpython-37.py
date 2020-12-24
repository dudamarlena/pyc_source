# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\model\stats\outcome_stats.py
# Compiled at: 2019-05-15 19:14:11
# Size of source mod 2**32: 665 bytes
from bets.model.stats.ratio_stats import RatioStats, OUTCOMES

class OutcomeStats(RatioStats):
    KEYS = RatioStats.KEYS + ['outcome', 'ratio', 'rank']
    outcome: str
    ratio: float
    rank: str

    def __init__(self, ratio_1, ratio_X, ratio_2, outcome, host_team='', guest_team='', date='', country='', tournament=''):
        super().__init__(ratio_1, ratio_X, ratio_2, host_team, guest_team, date, country, tournament)
        if outcome not in OUTCOMES:
            raise ValueError(outcome)
        self.outcome = outcome
        self.ratio = self[f"ratio_{outcome}"]
        self.rank = self[f"rank_{outcome}"]