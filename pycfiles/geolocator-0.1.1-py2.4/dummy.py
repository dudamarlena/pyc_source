# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\providers\dummy.py
# Compiled at: 2006-03-06 15:28:24
"""
Base (dummy) providers

"""
import os, sys

class CityDataProvider:
    __module__ = __name__

    def getCityByIp(self, ip):
        """get city name"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))

    def getCityByDomain(self, domain):
        """get city name"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))


class LocationDataProvider:
    """get coordinates"""
    __module__ = __name__

    def getLocationByIp(self, ip):
        """get country code"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))

    def getLocationByDomain(self, domain):
        """get country code"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))


class CountryDataProvider:
    """get country"""
    __module__ = __name__

    def getCountryByIp(self, ip):
        """get country code"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))

    def getCountryByDomain(self, domain):
        """get country code"""
        klass, func = self.__class__.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))


class Provider(CountryDataProvider, CityDataProvider, LocationDataProvider):
    """a dummy provider to be used when none can be used"""
    __module__ = __name__