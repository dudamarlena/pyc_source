# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/sale/tests/test.py
# Compiled at: 2016-12-30 20:18:19
# Size of source mod 2**32: 171 bytes
from django.test import TestCase

class AnimalTestCase(TestCase):

    def setUp(self):
        pass

    def test_animals_can_speak(self):
        self.assertEqual(1, 2)