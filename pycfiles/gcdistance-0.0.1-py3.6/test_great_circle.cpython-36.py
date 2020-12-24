# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gcdistance\tests\test_great_circle.py
# Compiled at: 2019-09-30 10:38:18
# Size of source mod 2**32: 415 bytes
"""
Created on Mon Sep 30 11:30:50 2019

@author: lealp
"""
from unittest import TestCase
from gcdistance.gcdistance import great_circle_distance

class Testgcdistance(TestCase):

    def test_distance(self):
        P1 = (1, 2)
        P2 = (2, 3)
        s = great_circle_distance(P1, P2)
        self.assertTrue(isinstance(s, float))