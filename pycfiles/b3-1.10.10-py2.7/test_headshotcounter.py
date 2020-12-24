# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\iourt42\test_headshotcounter.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class Test_headshotcounter(Iourt42TestCase):

    def setUp(self):
        super(Test_headshotcounter, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[headshotcounter]\n# enable the headshot counter?\nhs_enable: True\n# reset counts? Options: no / map / round\nreset_vars: no\n# set broadcast to True if you want the counter to appear in the upper left, False is in chatarea\nbroadcast: True\n# Announce every single headshot?\nannounce_all: True\n# Announce percentages (after 5 headshots)\nannounce_percentages: True\n# Only show percentages larger than next threshold\npercent_min: 10\n# Advise victims to wear a helmet?\nwarn_helmet: True\n# After how many headshots?\nwarn_helmet_nr: 7\n# Advise victims to wear kevlar?\nwarn_kevlar: True\n# After how many torso hits?\nwarn_kevlar_nr: 50\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.write = Mock()

    def test_hitlocation(self):

        def joe_hits_simon(hitloc):
            self.console.parseLine('Hit: 7 6 %s 8: Grover hit jacobdk92 in the Head' % hitloc)

        def assertCounts(head, helmet, torso):
            self.assertEqual(head, self.joe.var(self.p, 'headhits', default=0.0).value)
            self.assertEqual(helmet, self.joe.var(self.p, 'helmethits', default=0.0).value)
            self.assertEqual(torso, self.simon.var(self.p, 'torsohitted', default=0.0).value)

        self.joe.connects('6')
        self.simon.connects('7')
        joe_hits_simon('0')
        assertCounts(head=0.0, helmet=0.0, torso=0.0)
        joe_hits_simon('1')
        assertCounts(head=1.0, helmet=0.0, torso=0.0)
        joe_hits_simon('2')
        assertCounts(head=1.0, helmet=1.0, torso=0.0)
        joe_hits_simon('3')
        assertCounts(head=1.0, helmet=1.0, torso=1.0)