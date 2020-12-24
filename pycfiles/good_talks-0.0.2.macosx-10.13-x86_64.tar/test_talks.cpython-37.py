# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsmith/Projects/personal/presentations/2018/packaging_talk/venv/lib/python3.7/site-packages/talks/tests/test_talks.py
# Compiled at: 2018-09-25 19:18:34
# Size of source mod 2**32: 442 bytes
from talks import Talk
from unittest import TestCase

class TestTalk(TestCase):

    def setUp(self):
        self.talk = Talk()

    def test_thank(self):
        self.assertEqual(self.talk.thank(), 'Thanks!')

    def test_crowd(self):
        self.assertEqual(self.talk.thank(crowd='me'), 'Thanks for coming to me')

    def test_speaker(self):
        self.assertEqual(self.talk.thank(speaker='me'), 'Thanks you me for giving this talk')