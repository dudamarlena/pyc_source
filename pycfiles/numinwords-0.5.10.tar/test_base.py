# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_base.py
# Compiled at: 2020-04-17 01:12:09
from __future__ import unicode_literals
from decimal import Decimal
from unittest import TestCase
from numinwords.base import Num2Word_Base

class Num2WordBaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(Num2WordBaseTest, cls).setUpClass()
        cls.base = Num2Word_Base()

    def test_to_currency_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.base.to_currency(Decimal(b'1.00'), currency=b'EUR')

    def test_error_to_cardinal_float(self):
        from numinwords.base import Num2Word_Base
        with self.assertRaises(TypeError):
            Num2Word_Base.to_cardinal_float(9)
        with self.assertRaises(TypeError):
            Num2Word_Base.to_cardinal_float(b'a')

    def test_error_merge(self):
        from numinwords.base import Num2Word_Base
        self.base = Num2Word_Base()
        with self.assertRaises(NotImplementedError):
            self.base.merge(2, 3)

    def test_is_title(self):
        from numinwords.base import Num2Word_Base
        self.base = Num2Word_Base()
        self.assertEqual(self.base.title(b'one'), b'one')
        self.base.is_title = True
        self.assertEqual(self.base.title(b'one'), b'One')