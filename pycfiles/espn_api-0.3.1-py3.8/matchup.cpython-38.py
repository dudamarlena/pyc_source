# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/matchup.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 693 bytes


class Matchup(object):
    __doc__ = 'Creates Matchup instance'

    def __init__(self, data):
        self.data = data
        self._fetch_matchup_info()

    def __repr__(self):
        return 'Matchup(%s, %s)' % (self.home_team, self.away_team)

    def _fetch_matchup_info(self):
        """Fetch info for matchup"""
        self.home_team = self.data['home']['teamId']
        self.home_score = self.data['home']['totalPoints']
        self.away_team = 0
        self.away_score = 0
        if 'away' in self.data:
            self.away_team = self.data['away']['teamId']
            self.away_score = self.data['away']['totalPoints']