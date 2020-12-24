# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/glucose/test_display.py
# Compiled at: 2015-12-15 13:09:24
from unittest import TestCase
from openaps.glucose.display import Display

class DisplayTestCase(TestCase):
    """
        Checks that the display function rounds to the correct number
        of significant digits
    """

    def test_display_mmol_l(self):
        self.assertEqual(Display.display('mmol/L', 5.49), 5.5)
        self.assertEqual(Display.display('mmol/L', 5.500001), 5.5)
        self.assertEqual(Display.display('mmol/L', 5.51), 5.5)
        self.assertEqual(Display.display('mmol/L', 5.59), 5.6)

    def test_display_mg_dl(self):
        self.assertEqual(Display.display('mg/dL', 147.078), 147)
        self.assertEqual(Display.display('mg/dL', 268.236), 268)
        self.assertEqual(Display.display('mg/dL', 605.97), 606)
        self.assertEqual(Display.display('mg/dL', 623.268), 623)