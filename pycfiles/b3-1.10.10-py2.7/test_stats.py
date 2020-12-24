# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_stats.py
# Compiled at: 2015-02-24 17:29:43
from textwrap import dedent
from mockito import when
from b3 import TEAM_RED, TEAM_BLUE, TEAM_FREE
from b3.fake import FakeClient
from b3.plugins.admin import AdminPlugin
from tests import B3TestCase, logging_disabled
from b3.plugins.stats import StatsPlugin
from b3.config import CfgConfigParser

class Test_config(B3TestCase):

    def test_empty(self):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n        '))
        self.p = StatsPlugin(self.console, conf)
        self.p.onLoadConfig()
        self.assertEqual(0, self.p.mapstatslevel)
        self.assertEqual(0, self.p.testscorelevel)
        self.assertEqual(2, self.p.topstatslevel)
        self.assertEqual(2, self.p.topxplevel)
        self.assertEqual(100, self.p.startPoints)
        self.assertFalse(self.p.resetscore)
        self.assertFalse(self.p.resetxp)
        self.assertFalse(self.p.show_awards)
        self.assertFalse(self.p.show_awards_xp)

    def test_nominal(self):
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [commands]\n            mapstats-stats: 2\n            testscore-ts: 2\n            topstats-top: 20\n            topxp: 20\n\n            [settings]\n            startPoints: 150\n            resetscore: yes\n            resetxp: yes\n            show_awards: yes\n            show_awards_xp: yes\n        '))
        self.p = StatsPlugin(self.console, conf)
        self.p.onLoadConfig()
        self.assertEqual(2, self.p.mapstatslevel)
        self.assertEqual(2, self.p.testscorelevel)
        self.assertEqual(20, self.p.topstatslevel)
        self.assertEqual(20, self.p.topxplevel)
        self.assertEqual(150, self.p.startPoints)
        self.assertTrue(self.p.resetscore)
        self.assertTrue(self.p.resetxp)
        self.assertTrue(self.p.show_awards)
        self.assertTrue(self.p.show_awards_xp)


class StatPluginTestCase(B3TestCase):

    def setUp(self):
        B3TestCase.setUp(self)
        with logging_disabled():
            admin_conf = CfgConfigParser()
            admin_plugin = AdminPlugin(self.console, admin_conf)
            admin_plugin.onLoadConfig()
            admin_plugin.onStartup()
            when(self.console).getPlugin('admin').thenReturn(admin_plugin)
        conf = CfgConfigParser()
        conf.loadFromString(dedent('\n            [commands]\n            mapstats-stats: 0\n            testscore-ts: 0\n            topstats-top: 0\n            topxp: 0\n\n            [settings]\n            startPoints: 100\n            resetscore: no\n            resetxp: no\n            show_awards: no\n            show_awards_xp: no\n        '))
        self.p = StatsPlugin(self.console, conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=1, team=TEAM_RED)
        self.mike = FakeClient(self.console, name='Mike', guid='mikeguid', groupBits=1, team=TEAM_RED)
        self.joe.connects(1)
        self.mike.connects(2)


class Test_score(StatPluginTestCase):

    def test_no_points(self):
        self.joe.setvar(self.p, 'points', 0)
        self.mike.setvar(self.p, 'points', 0)
        s = self.p.score(self.joe, self.mike)
        self.assertEqual(12.5, s)

    def test_equal_points(self):
        self.joe.setvar(self.p, 'points', 50)
        self.mike.setvar(self.p, 'points', 50)
        s = self.p.score(self.joe, self.mike)
        self.assertEqual(12.5, s)

    def test_victim_has_more_points(self):
        self.joe.setvar(self.p, 'points', 50)
        self.mike.setvar(self.p, 'points', 100)
        s = self.p.score(self.joe, self.mike)
        self.assertEqual(20.0, s)

    def test_victim_has_less_points(self):
        self.joe.setvar(self.p, 'points', 100)
        self.mike.setvar(self.p, 'points', 50)
        s = self.p.score(self.joe, self.mike)
        self.assertEqual(8.75, s)


class Test_cmd_mapstats(StatPluginTestCase):

    def test_no_activity(self):
        self.joe.says('!mapstats')
        self.assertListEqual(['Stats [ Joe ] K 0 D 0 TK 0 Dmg 0 Skill 100.00 XP 0.0'], self.joe.message_history)

    def test_tk(self):
        self.joe.kills(self.mike)
        self.joe.says('!mapstats')
        self.assertListEqual(['Stats [ Joe ] K 0 D 0 TK 1 Dmg 0 Skill 87.50 XP 0.0'], self.joe.message_history)
        self.mike.says('!mapstats')
        self.assertListEqual(['Stats [ Mike ] K 0 D 0 TK 0 Dmg 0 Skill 100.00 XP 0.0'], self.mike.message_history)

    def test_kill(self):
        self.joe.team = TEAM_BLUE
        self.mike.team = TEAM_RED
        self.joe.kills(self.mike)
        self.joe.says('!mapstats')
        self.assertListEqual(['Stats [ Joe ] K 1 D 0 TK 0 Dmg 100 Skill 112.50 XP 12.5'], self.joe.message_history)
        self.mike.says('!mapstats')
        self.assertListEqual(['Stats [ Mike ] K 0 D 1 TK 0 Dmg 0 Skill 87.50 XP 0.0'], self.mike.message_history)


class Test_cmd_testscore(StatPluginTestCase):

    def test_no_data(self):
        self.joe.says('!testscore')
        self.assertListEqual(['You must supply a player name to test'], self.joe.message_history)

    def test_self(self):
        self.joe.says('!testscore joe')
        self.assertListEqual(["You don't get points for killing yourself"], self.joe.message_history)

    def test_teammate(self):
        assert self.joe.team == self.mike.team
        self.joe.says('!testscore mike')
        self.assertListEqual(["You don't get points for killing a team mate"], self.joe.message_history)

    def test_no_team(self):
        self.joe.team = TEAM_FREE
        self.mike.team = TEAM_FREE
        assert self.joe.team == self.mike.team
        self.joe.says('!testscore mike')
        self.assertListEqual(['Stats: Joe will get 12.5 skill points for killing Mike'], self.joe.message_history)

    def test_enemy(self):
        self.joe.team = TEAM_BLUE
        assert self.joe.team != self.mike.team
        self.joe.says('!testscore mike')
        self.assertListEqual(['Stats: Joe will get 12.5 skill points for killing Mike'], self.joe.message_history)


class Test_cmd_topstats(StatPluginTestCase):

    def test_no_data(self):
        self.joe.says('!topstats')
        self.assertListEqual(['Stats: No top players'], self.joe.message_history)

    def test_teammate(self):
        assert self.joe.team == self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topstats')
        self.assertListEqual(['Top Stats: #1 Mike [100.0], #2 Joe [87.5]'], self.joe.message_history)

    def test_no_team(self):
        self.joe.team = TEAM_FREE
        self.mike.team = TEAM_FREE
        assert self.joe.team == self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topstats')
        self.assertListEqual(['Top Stats: #1 Mike [100.0], #2 Joe [87.5]'], self.joe.message_history)

    def test_enemy(self):
        self.joe.team = TEAM_BLUE
        assert self.joe.team != self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topstats')
        self.assertListEqual(['Top Stats: #1 Joe [112.5], #2 Mike [87.5]'], self.joe.message_history)


class Test_cmd_topxp(StatPluginTestCase):

    def test_no_data(self):
        self.joe.says('!topxp')
        self.assertListEqual(['Stats: No top experienced players'], self.joe.message_history)

    def test_teammate(self):
        assert self.joe.team == self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topxp')
        self.assertListEqual(['Top Experienced Players: #1 Mike [0.0], #2 Joe [-0.0]'], self.joe.message_history)

    def test_no_team(self):
        self.joe.team = TEAM_FREE
        self.mike.team = TEAM_FREE
        assert self.joe.team == self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topxp')
        self.assertListEqual(['Top Experienced Players: #1 Mike [0.0], #2 Joe [-0.0]'], self.joe.message_history)

    def test_enemy(self):
        self.joe.team = TEAM_BLUE
        assert self.joe.team != self.mike.team
        self.joe.kills(self.mike)
        self.joe.says('!topxp')
        self.assertListEqual(['Top Experienced Players: #1 Joe [12.5], #2 Mike [-0.0]'], self.joe.message_history)