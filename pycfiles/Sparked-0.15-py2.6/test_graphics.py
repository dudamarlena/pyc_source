# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/test/test_graphics.py
# Compiled at: 2010-12-21 15:42:19
"""
Tests for sparked.graphics.*

Maintainer: Arjan Scherpenisse
"""
from twisted.trial import unittest
from sparked.graphics import util

class TestGraphicsUtil(unittest.TestCase):
    """
    Test the L{sparked.monitors.MonitorContainer}
    """

    def testParseColor(self):
        map = [
         ((0, 0, 0), '000000'),
         ((0, 0, 0), '000'),
         ((0, 0, 0), '#000000'),
         ((0, 0, 0), '#000'),
         ((1, 1, 1), 'FFFFFF'),
         ((1, 1, 1), 'FFF'),
         ((1, 1, 1), '#FFFFFF'),
         ((1, 1, 1), '#FFF')]
        [ self.assertEqual(a, util.parseColor(b)) for (a, b) in map ]