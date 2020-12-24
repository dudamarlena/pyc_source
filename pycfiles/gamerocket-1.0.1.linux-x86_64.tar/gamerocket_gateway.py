# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/gamerocket_gateway.py
# Compiled at: 2013-08-07 10:45:10
from action_gateway import ActionGateway
from achievement_gateway import AchievementGateway
from game_gateway import GameGateway
from player_gateway import PlayerGateway
from purchase_gateway import PurchaseGateway

class GamerocketGateway(object):

    def __init__(self, config):
        self.config = config
        self.achievement = AchievementGateway(self)
        self.action = ActionGateway(self)
        self.game = GameGateway(self)
        self.player = PlayerGateway(self)
        self.purchase = PurchaseGateway(self)