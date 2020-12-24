# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/pick.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 669 bytes


class Pick(object):
    __doc__ = ' Pick represents a pick in draft '

    def __init__(self, team, playerId, playerName, round_num, round_pick, bid_amount, keeper_status):
        self.team = team
        self.playerId = playerId
        self.playerName = playerName
        self.round_num = round_num
        self.round_pick = round_pick
        self.bid_amount = bid_amount
        self.keeper_status = keeper_status

    def __repr__(self):
        return 'Pick(%s, %s)' % (self.playerName, self.team)

    def auction_repr(self):
        return ', '.join(map(str, [self.team.owner, self.playerId, self.playerName, self.bid_amount, self.keeper_status]))