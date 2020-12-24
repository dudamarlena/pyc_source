# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test.py
# Compiled at: 2011-10-20 14:07:08
import unittest, logging
from test_data import TEXTS
from droopy.factory import DroopyFactory

class TestAll(unittest.TestCase):
    """All processors test merged into one test. See module test_data"""

    def test_run(self):
        for test_text in TEXTS:
            lang_class = test_text.pop('lang')
            id = test_text.pop('id')
            text = test_text.pop('text')
            droopy = DroopyFactory.create_full_droopy(text, lang_class())
            for proc in test_text:
                expected = round(test_text[proc], 2)
                got = round(getattr(droopy, proc), 2)
                if not expected == got:
                    self.fail('Inccorect value in text %s for processor %s (%s). Expected %s, got %s' % (id, proc, droopy.lang, expected, got))