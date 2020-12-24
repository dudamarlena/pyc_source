# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\providers\gns.py
# Compiled at: 2006-03-06 15:28:24
"""
 This provider is initialized with the path to the directory containing data files

"""
import os
__all__ = [
 'GnsProvider']

class GnsProvider:
    """GeoNameServer data provider"""
    __module__ = __name__

    def getLocationByCity(self):
        """"""
        klass, func = self.__class.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))

    def getLocationByCountry(self):
        """"""
        klass, func = self.__class.__name__, sys._getframe().f_code.co_name
        raise NotImplementedError('%s is not implemented by %s.' % (func, klass))


if __name__ == '__main__':

    def firstValidPath(candidates):
        for i in candidates:
            if os.path.exists(i):
                return i


    MMCountryFile = 'GeoIP.dat'
    MMCityFile = 'GeoIPCity.dat'
    unixpth = '/usr/local/share/GeoIP/'
    pkgpth = os.path.abspath(os.curdir) + os.sep + 'data' + os.sep
    candidates = None
    curdir = os.path.abspath(os.curdir)
    if os.name == 'posix':
        candidates = (
         pkgpth + MMCityFile, pkgpth + MMCountryFile, unixpth + MMCityFile, unixpth + MMCountryFile)
    else:
        candidates = (
         pkgpth + MMCityFile, pkgpth + MMCountryFile)
    datafile = firstValidPath(candidates)
    print 'Using %s as data source' % datafile
    ip = '157.24.8.108'
    if MMCountryFile in datafile:
        l = GeoLocator(MMCountryIPProvider, datafile)
        assert l.getCountryByIP(ip) == 'FI'
    elif MMCityFile in datafile:
        l = GeoLocator(MMCityIPProvider, datafile)
        assert l.getCityByIP(ip) == 'Lappeenranta'