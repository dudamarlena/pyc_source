# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\stats\test_score.py
# Compiled at: 2016-03-08 18:42:10
from tests.plugins.stats import StatPluginTestCase

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