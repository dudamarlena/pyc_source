# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\tests\geolocatortests.py
# Compiled at: 2006-03-06 15:28:22
"""
 Unit tests. Add more!
"""
import unittest
from geolocator import GeoLocator
from geolocator.providers import DummyProvider
from geolocator.providers import MaxMindCityIpProvider
from geolocator.providers import MaxMindCountryIpProvider
__all__ = ('GeolocatorTestSuite', )

class DummyLocatorCase(unittest.TestCase):
    """test the default"""
    __module__ = __name__

    def setUp(self):
        self.locator = GeoLocator()
        self.provider = MaxMindCityDataProvider()
        self.city = 'Munkkiniemi'
        self.country = 'FI'
        self.domain = 'www.helsinki.fi'
        self.ip = '128.214.205.16'

    def tearDown(self):
        del self.locator

    def testCityForIp(self):
        self.assertRaises(self.locator.getCityForIp(self.ip), NotImplementedError)

    def testCityForDomain(self):
        self.assertRaises(self.locator.getCityForDomain(self.domain), NotImplementedError)

    def testCountryForIp(self):
        self.assertRaises(self.locator.getCountryForIp(self.ip), NotImplementedError)

    def testCountryForDomain(self):
        self.assertRaises(self.locator.getCountryForDomain(self.domain), NotImplementedError)

    def testCoordinatesForIp(self):
        self.assertRaises(self.locator.getCityForIp(self.ip), NotImplementedError)

    def testCoordinatesForDomain(self):
        self.assertRaises(self.locator.getCityForDomain(self.domain), NotImplementedError)


class MaxMindCountryProviderCase:
    __module__ = __name__

    def testCountryForIp(self):
        self.assertRaises(self.locator.getCountryForIp(self.ip), NotImplementedError)

    def testCountryForDomain(self):
        self.assertRaises(self.locator.getCountryForDomain(self.domain), NotImplementedError)


GeolocatorTestSuite = unittest.makeSuite(DummyProviderCase, 'test')
if __name__ == '__main__':
    unittest.main()
    raw_input('press any key to quit...')