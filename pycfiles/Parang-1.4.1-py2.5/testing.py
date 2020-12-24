# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parang/testing.py
# Compiled at: 2009-08-22 22:50:09
"""Test cases for Parang bots
    Copyright (C) 2004-2008  Eric Wald
    
    This software may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this software for
    commercial purposes without permission from the authors is prohibited.
"""
import unittest
from parlance.config import variants
from parlance.functions import Infinity
from parlance.gameboard import Variant
from parlance.language import protocol
from parlance.tokens import *
from parlance.player import HoldBot
from parlance.xtended import *
from parlance.test.player import BotTestCase
from parlance.test.network import NetworkTestCase
from parang.blabberbot import BlabberBot
from parang.combobot import ComboBot
from parang.dumbbot import DumbBot
from parang.evilbot import EvilBot
from parang.neurotic import Neurotic
from parang.peacebot import PeaceBot
from parang.project20m import Project20M
from parang.teddybot import TeddyBot

class BlabberBotTestCase(BotTestCase):
    bot_class = BlabberBot

    def test_alone(self):
        self.variant = alone = Variant('alone')
        information = '\n            [homes]\n            ENG=LON\n            [ownership]\n            ENG=LON\n            [borders]\n            WAL=AMY LON, FLT ECH\n            LON=AMY WAL, FLT ECH NTH\n            ECH=FLT NTH LON WAL\n            NTH=FLT ECH LON\n        '
        alone.parse((line.strip() for line in information.splitlines()))
        alone.rep = alone.tokens()
        self.failUnlessComplete(None, None, alone.rep['ENG'])
        return

    def test_seasons(self):
        self.start_game()
        season = self.player.random_category('Phases')
        self.failUnlessEqual(season.category, protocol.token_cats['Phases'])


class DumbBotTestCase(BotTestCase):
    bot_class = DumbBot


class ComboBotTestCase(BotTestCase):
    bot_class = ComboBot


class EvilBotTestCase(BotTestCase):
    bot_class = EvilBot


class NeuroticTestCase(BotTestCase):
    bot_class = Neurotic

    def setUp(self):
        BotTestCase.setUp(self)
        self.variant = variants['hundred3']

    def test_neurotic_duplication(self):
        self.connect_player(Neurotic)
        self.start_game()
        first_result = [ message for message in self.replies if message[0] == SUB
                       ]
        self.replies = []
        self.send(self.variant.start_now)
        second_result = [ message for message in self.replies if message[0] == SUB
                        ]
        self.failUnlessEqual(first_result, second_result)


class PeaceBotTestCase(BotTestCase):
    bot_class = PeaceBot


class TeddyBotTestCase(BotTestCase):
    bot_class = TeddyBot

    def assertOrder(self, now, sco, country, order):
        self.assertOrders(now, sco, country, [order])

    def assertOrders(self, now, sco, country, orders):
        self.start_game(now, sco, country)
        obtained = sum((msg.fold()[1:] for msg in self.replies if msg[0] is SUB), [])
        for order in orders:
            self.assertContains(order, obtained)

    def test_neutral_opportunity(self):
        now = NOW(FAL, 1901)(TUR, AMY, CON)
        expected = [[TUR, AMY, CON], MTO, BUL]
        self.assertOrder(now, None, TUR, expected)
        return

    def test_central_opportunity(self):
        now = NOW(FAL, 1901)(TUR, AMY, LVN)
        expected = [[TUR, AMY, LVN], MTO, WAR]
        self.assertOrder(now, None, TUR, expected)
        return

    def test_island_opportunity(self):
        now = NOW(FAL, 1901)(TUR, FLT, WAL)
        expected = [[TUR, FLT, WAL], MTO, LON]
        self.assertOrder(now, None, TUR, expected)
        return

    def test_unopposed_opportunity(self):
        now = NOW(FAL, 1901)(TUR, AMY, BUR)(GER, AMY, KIE)(FRA, AMY, GAS)
        expected = [[TUR, AMY, BUR], MTO, BEL]
        self.assertOrder(now, None, TUR, expected)
        return

    def test_unowned_opportunity(self):
        now = NOW(FAL, 1901)(TUR, AMY, BUR)
        sco = SCO(AUS, BUD, TRI, VIE)(ENG, LVP, EDI, LON)(FRA, BRE, PAR)(GER, KIE, BER)(ITA, ROM, NAP, VEN)(RUS, STP, MOS, WAR, SEV)(TUR, ANK, CON, SMY, MAR, MUN, BEL)(UNO, NWY, SWE, DEN, HOL, SPA, POR, TUN, GRE, SER, RUM, BUL)
        expected = [[TUR, AMY, BUR], MTO, PAR]
        self.assertOrder(now, sco, TUR, expected)

    def test_leader_opportunity(self):
        now = NOW(FAL, 1901)(TUR, AMY, BUR)
        sco = SCO(AUS, BUD)(ENG, EDI, LVP, LON, BEL)(FRA, BRE, PAR)(GER, KIE, BER, MUN)(ITA, ROM, NAP, VEN, TRI, VIE, MAR, DEN, HOL, SPA, POR, TUN, GRE, SER, RUM, BUL, MOS, WAR)(RUS, STP, SEV)(TUR, ANK, CON, SMY)(UNO, NWY, SWE)
        expected = [[TUR, AMY, BUR], MTO, MAR]
        self.assertOrder(now, sco, TUR, expected)

    def test_build_fleet(self):
        now = NOW(WIN, 1901)(ENG, AMY, YOR)(ENG, AMY, WAL)
        expected = [[ENG, FLT, LON], BLD]
        self.assertOrder(now, None, ENG, expected)
        return

    def test_two_armies(self):
        now = NOW(WIN, 1901)(AUS, FLT, TRI)
        expected = [[[AUS, AMY, VIE], BLD],
         [
          [
           AUS, AMY, BUD], BLD]]
        self.assertOrders(now, None, AUS, expected)
        return


class CentralityTestCase(unittest.TestCase):
    """Low-level unit tests for TeddyBot's internal calculations.
        Currently tests its distance and centrality computations.
    """
    bot_class = TeddyBot

    def setUp(self):
        player = self.bot_class(send_method=self.handle_message, representation=standard.rep)
        player.map = standard_map
        self.distance = player.calc_distances()
        self.centrality = player.calc_centrality(self.distance)

    def handle_message(self, message):
        pass

    def test_fleet_distance(self):
        dist = self.distance[((FLT, POR, None), (FLT, FIN, None))]
        self.failUnlessEqual(dist, 6)
        return

    def test_fleet_distance_coastal(self):
        dist = self.distance[((FLT, SPA, NCS), (FLT, PIE, None))]
        self.failUnlessEqual(dist, 4)
        return

    def test_fleet_distance_coastal_crawl(self):
        dist = self.distance[((FLT, MAR, None), (FLT, GAS, None))]
        self.failUnlessEqual(dist, 3)
        return

    def test_fleet_distance_self(self):
        dist = self.distance[((FLT, POR, None), (FLT, POR, None))]
        self.failUnlessEqual(dist, 0)
        return

    def test_army_distance(self):
        dist = self.distance[((AMY, POR, None), (AMY, FIN, None))]
        self.failUnlessEqual(dist, 8)
        return

    def test_army_distance_infinity(self):
        dist = self.distance[((AMY, TUN, None), (AMY, NAP, None))]
        self.failUnlessEqual(dist, Infinity)
        return

    def test_army_distance_self(self):
        dist = self.distance[((AMY, POR, None), (AMY, POR, None))]
        self.failUnlessEqual(dist, 0)
        return

    def test_convoy_distance(self):
        dist = self.distance[(POR, FIN)]
        self.failUnlessEqual(dist, 5)

    def test_convoy_distance_self(self):
        dist = self.distance[(POR, POR)]
        self.failUnlessEqual(dist, 0)

    def test_land_centrality(self):
        self.failUnless(self.centrality[MUN] > self.centrality[SYR])


class HuffTestCase(BotTestCase):
    bot_class = Project20M


class FullBotGames(NetworkTestCase):
    """Functional tests, pitting bots against each other."""

    def test_one_dumbbot(self):
        """ Six drawing holdbots and a dumbbot"""
        self.set_verbosity(1)
        self.connect_server([DumbBot, HoldBot, HoldBot,
         HoldBot, HoldBot, HoldBot, HoldBot])

    def test_dumbbots(self):
        """ seven dumbbots, quick game"""
        self.set_verbosity(5)
        self.connect_server([DumbBot] * 7)

    def test_evilbots(self):
        """ Six drawing evilbots and a holdbot"""
        self.set_verbosity(4)
        EvilBot.games.clear()
        self.connect_server([HoldBot, EvilBot, EvilBot,
         EvilBot, EvilBot, EvilBot, EvilBot])

    def test_neurotic(self):
        """ One Neurotic against two EvilBots."""
        self.set_verbosity(14)
        self.set_option('send_ORD', True)
        self.set_option('variant', 'hundred3')
        self.set_option('quit', True)
        EvilBot.games.clear()
        self.connect_server([Neurotic, EvilBot, EvilBot])


if __name__ == '__main__':
    unittest.main()