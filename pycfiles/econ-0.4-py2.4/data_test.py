# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/data_test.py
# Compiled at: 2007-04-18 06:57:54
import unittest, StringIO
from data import *

class TimeSeriesTest(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.data = [
         (1989, 4.4), (1990, 5.2), (1991, 5.3)]
        self.ts1 = TimeSeries(self.data)

    def testGetValue(self):
        self.assertEquals(self.ts1.getValue(1991), 5.3)

    def testGetValueOutsideRange(self):
        self.assertRaises(ValueError, self.ts1.getValue, 1986)

    def testGetValueInterpolated(self):
        self.assertEquals(self.ts1.getValue(1990.5), 5.25)

    def testGetTimeSeriesFromCsv(self):
        csvData = '1850,10.9\n1851,10.6\n1852,10.6\n1853,11.5'
        csvDataFileObject = StringIO.StringIO(csvData)
        ts1 = getTimeSeriesFromCsv(csvDataFileObject)
        self.assertEquals(ts1.getValue(1850), 10.9)