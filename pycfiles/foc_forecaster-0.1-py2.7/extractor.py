# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/tests/extractor.py
# Compiled at: 2011-12-21 07:09:55
"""
Created on 16. 12. 2011.

@author: kermit
"""
import unittest
from forecaster.sources.extractor import Extractor
from forecaster.common import conf

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.extractor = Extractor()

    def test_fetch_data(self):
        countries = self.extractor.fetch_data_per_conf(conf)
        self.assertTrue(len(countries) > 0)

    def test_fetch_indicator(self):
        indicator = self.extractor.fetch_indicator('hrv', 'SP.POP.TOTL', 1998, 1999)
        self.assertEqual(indicator.get_values(), [4501000.0, 4554000.0])
        self.assertEqual(indicator.get_dates(), [1998, 1999])


if __name__ == '__main__':
    unittest.main()