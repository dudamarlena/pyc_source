# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/base_settings.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 857 bytes


class BaseSettings(object):
    __doc__ = 'Creates Settings object'

    def __init__(self, data):
        self.reg_season_count = data['scheduleSettings']['matchupPeriodCount']
        self.veto_votes_required = data['tradeSettings']['vetoVotesRequired']
        self.team_count = data['size']
        self.playoff_team_count = data['scheduleSettings']['playoffTeamCount']
        self.keeper_count = data['draftSettings']['keeperCount']
        self.trade_deadline = 0
        if 'deadlineDate' in data['tradeSettings']:
            self.trade_deadline = data['tradeSettings']['deadlineDate']
        self.name = data['name']
        self.tie_rule = data['scoringSettings']['matchupTieRule']
        self.playoff_seed_tie_rule = data['scoringSettings']['playoffMatchupTieRule']

    def __repr__(self):
        return 'Settings(%s)' % self.name