# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\geolocator.py
# Compiled at: 2006-03-06 15:28:24
import os, gislib
from providers import *
__all__ = [
 'DummyLocator', 'MaxMindCountryLocator', 'MaxMindCityLocator']

class GeoLocatorBase:
    __module__ = __name__

    def getDistance(self, origin, location):
        """get distance between origin and location"""
        return gislib.getDistanceByHaversine(origin, location)

    def isWithinDistance(origin, location, distance):
        """return true if location is within the given distance from origin"""
        return gislib.isWithinDistance(origin, location, distance)


class DummyLocator(GeoLocatorBase, DummyProvider):
    """generic proxy/api to various data sources"""
    __module__ = __name__


class MaxMindCountryLocator(GeoLocatorBase, MaxMindCountryDataProvider):
    """for using the free country data"""
    __module__ = __name__


class MaxMindCityLocator(GeoLocatorBase, MaxMindCityDataProvider):
    """for using the commercial city data"""
    __module__ = __name__