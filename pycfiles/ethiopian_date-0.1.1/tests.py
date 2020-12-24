# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ethiopian_date/tests.py
# Compiled at: 2010-12-22 09:27:28
import unittest
from datetime import date
from ethiopian_date import EthiopianDateConverter

class TestEthiopianCalendar(unittest.TestCase):

    def test_gregorian_to_ethiopian(self):
        conv = EthiopianDateConverter.to_ethiopian
        self.assertEqual(conv(1982, 11, 21).strftime('%F'), '1975-03-12')
        self.assertEqual(conv(1941, 12, 7).strftime('%F'), '1934-03-28')
        self.assertEqual(conv(2010, 12, 22).strftime('%F'), '2003-04-13')

    def test_ethiopian_to_gregorian(self):
        conv = EthiopianDateConverter.to_gregorian
        self.assertEqual(conv(2003, 4, 11).strftime('%F'), '2010-12-20')
        self.assertEqual(conv(1975, 3, 12).strftime('%F'), '1982-11-21')


if __name__ == '__main__':
    unittest.main()