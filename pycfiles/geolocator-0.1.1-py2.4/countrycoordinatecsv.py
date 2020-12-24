# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\providers\countrycoordinatecsv.py
# Compiled at: 2006-03-06 15:28:24
import os

class CountryLocationProvider:
    """"""
    __module__ = __name__
    FILENAME = 'countrylocations.csv'

    def __init__(self):
        self.countrylocations = {}
        file = open(os.path.abspath(os.curdir) + os.sep + FILENAME)
        for l in file:
            (countrycode, latitude, longitude) = l.split(',')
            self.countrylocations[countrycode] = (latitude, longitude)

    def getLocationByCountry(self, countrycode):
        """get (latitude, longitude) tuple"""
        return self.countrylocations[countrycode]

    def locateCountry(self, countrycode):
        """get (latitude, longitude) tuple"""
        return self.getLocationByCountry(countrycode)