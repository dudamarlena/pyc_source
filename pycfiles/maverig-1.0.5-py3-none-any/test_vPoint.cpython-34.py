# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\tests\test_vPoint.py
# Compiled at: 2014-10-29 05:11:43
# Size of source mod 2**32: 1284 bytes
from unittest import TestCase
from maverig.views.positioning.vPoint import VPoint, Change
from PySide.QtCore import QPointF

class TestVPoint(TestCase):

    def setUp(self):
        self.vp1 = VPoint()
        self.vp2 = VPoint()

    def test_set_pos(self):
        self.vp1.set_pos(QPointF(1, 1), Change.moved)
        assert self.vp1.pos == QPointF(1, 1)

    def test_move_pos(self):
        self.vp1.pos = QPointF(1, 1)
        self.vp1.move_pos(QPointF(33, 1), Change.applied)
        assert self.vp1.pos == QPointF(33, 1) + QPointF(1, 1)

    def test_follow_follows(self):
        self.vp2.follow(self.vp1)
        follower = self.vp2.follows(self.vp1)
        assert follower is True

    def test_unfollow(self):
        self.vp1.follow(self.vp2)
        self.vp1.unfollow(self.vp2)
        assert self.vp1 not in self.vp2.followers

    def test_fix(self):
        self.vp2.fix(self.vp1)
        assert self.vp2 in self.vp1.followers and self.vp1 in self.vp2.followers

    def test_unfix(self):
        self.vp2.fix(self.vp1)
        assert self.vp2 in self.vp1.followers and self.vp1 in self.vp2.followers
        self.vp1.unfix(self.vp2)
        assert self.vp2 not in self.vp1.followers and self.vp1 not in self.vp2.followers