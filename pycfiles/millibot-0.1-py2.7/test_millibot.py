# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/millibot/tests/test_millibot.py
# Compiled at: 2017-01-12 02:05:19
from unittest import TestCase
from millibot import MilliBot

class MilliBotTests(TestCase):

    def setUp(self):
        self.millibot = MilliBot('Awesome Bot')

    def test_get_response(self):
        self.assertEqual(self.millibot.get_response('Hi'), 'Hi')