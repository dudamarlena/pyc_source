# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\interfaces.py
# Compiled at: 2006-03-06 15:28:24
"""
 Data provider interfaces.

  - IP should be given as a 'xxx.xxx.xxx.xxx' string

  - location is returned as a (lat,lon) tuple, where lat & lon are (degrees,minutes,seconds) tuples

  - city is identified by name, whereas a country is identified by country code

"""

class IGeoIPLocationProvider:
    """provides location by IP"""
    __module__ = __name__

    def getLocationByIP(ip):
        """get location"""
        pass


class ICityIPProvider:
    """provides city IP data"""
    __module__ = __name__

    def getCityByIP(ip):
        """"""
        pass


class ICountryIPProvider:
    """provides country IP data"""
    __module__ = __name__

    def getCountryByIP(ip):
        """"""
        pass


class IGeoLocationProvider:
    """provides city & country location data"""
    __module__ = __name__

    def getLocationByCity(cityname):
        """"""
        pass

    def getLocationByCountry(countrycode):
        """"""
        pass


class ICityNameProvider:
    """get city name"""
    __module__ = __name__

    def getCityName(cityname, language):
        """"""
        pass


class ICountryNameProvider:
    """get country name"""
    __module__ = __name__

    def getCountryName(countrycode, language):
        """"""
        pass