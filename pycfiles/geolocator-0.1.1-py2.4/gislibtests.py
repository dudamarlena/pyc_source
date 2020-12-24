# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\tests\gislibtests.py
# Compiled at: 2006-03-06 15:28:22
"""
 Unit tests. Add more!
"""
import unittest
from geolocator import gislib
__all__ = ('GislibTestSuite', )

class GisLibCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.oxlat = 51.752279
        self.oxlon = -1.255856
        self.distance = 70.0
        (lat, lon) = gislib.getCoordinatesForDistance(self.oxlat, self.oxlon, self.distance)
        self.lat_extra, self.lon_extra = lat, lon

    def tearDown(self):
        pass

    def testCalculateDistanceToEast(self):
        """make sure we can calculate eastbound distances ok"""
        loc1 = (
         self.oxlat, self.oxlon)
        loc2 = (self.oxlat, self.oxlon + self.lon_extra)
        d = gislib.getDistance(loc1, loc2)
        self.assertEqual(round(d, 1), self.distance)

    def testCalculateDistanceToWest(self):
        """make sure we can calculate westbound distances ok"""
        loc1 = (
         self.oxlat, self.oxlon)
        loc2 = (self.oxlat, self.oxlon - self.lon_extra)
        d = gislib.getDistance(loc1, loc2)
        self.assertEqual(round(d, 1), self.distance)

    def testCalculateDistanceToSouth(self):
        """make sure we can calculate southbound distances ok"""
        loc1 = (
         self.oxlat, self.oxlon)
        loc2 = (self.oxlat - self.lat_extra, self.oxlon)
        d = gislib.getDistance(loc1, loc2)
        self.assertEqual(round(d, 1), self.distance)

    def testCalculateDistanceToNorth(self):
        """make sure we can calculate northbound distances ok"""
        loc1 = (
         self.oxlat, self.oxlon)
        loc2 = (self.oxlat + self.lat_extra, self.oxlon)
        d = gislib.getDistance(loc1, loc2)
        self.assertEqual(round(d, 1), self.distance)

    def testCornerIsFurtherThanSide(self):
        """make sure the corner of bounding box is further than side (circle radius)"""
        loc1 = (
         self.oxlat, self.oxlon + self.lon_extra)
        loc2 = (self.oxlat + self.lat_extra, self.oxlon)
        d = gislib.getDistance(loc1, loc2)
        assert round(d, 1) > self.distance

    def testDistanceCalculations(self):
        kouvola = (60.52, -26.43)
        lpr = (61.03, -28.12)
        turku = (60.3, -22.19)
        helsinki = (60.15, -25.03)
        self.assertEqual(round(gislib.getDistanceByHaversine(turku, helsinki)), 158.0)
        self.assertEqual(round(gislib.getDistanceByHaversine(lpr, kouvola)), 108.0)


GislibTestSuite = unittest.makeSuite(GisLibCase, 'test')
if __name__ == '__main__':
    unittest.main()
    raw_input('press any key to quit...')