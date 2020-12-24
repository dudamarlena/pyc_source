# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\providers\maxmind.py
# Compiled at: 2006-03-06 15:28:24
"""
  Data provider implementations

   - MaxMind providers are initialized with the path to the binary database.

"""
import os
__all__ = [
 'CountryProvider', 'CityProvider']
LOCATIONS = ('./data', '/usr/share/GeoIP', '/usr/local/share/GeoIP')
COUNTRYDATA_FILENAME = 'GeoIP.dat'
CITYDATA_FILENAME = 'GeoIPCity.dat'

class BaseProvider:
    """base class"""
    __module__ = __name__

    def __init__(self, filepath=None, init_type='GEOIP_MEMORY_CACHE'):
        try:
            import GeoIP
        except Exception, e:
            hlp = '(note that you need both the C library & the Python extension)'
            raise Exception('GeoIP python extension could not be imported: %s\n%s' % (e, hlp))

        if filepath == None:
            for location in LOCATIONS:
                try:
                    filepath = location + os.sep + self.filename
                    file = open(filepath)
                    file.close()
                    break
                except:
                    pass

        try:
            import GeoIP
            self.database = GeoIP.open(filepath, getattr(GeoIP, init_type))
        except Exception, e:
            raise Exception('could not open MaxMind data: %s' % e)

        return


class CountryProvider(BaseProvider):
    """
   Provider for the free MaxMind country IP data
   """
    __module__ = __name__
    filename = COUNTRYDATA_FILENAME

    def getCountryByIp(self, ip):
        """return the country code"""
        return self.database.country_code_by_addr(ip)

    def getCountryByDomain(self, domain):
        """return country code"""
        return self.database.country_code_by_name(domain)


class CityProvider(BaseProvider):
    """Provider for the commercial MaxMind city data"""
    __module__ = __name__
    filename = CITYDATA_FILENAME

    def getCityByIp(self, ip):
        """get city name"""
        return self.database.record_by_addr(ip)['city']

    def getCityByDomain(self, domain):
        """get city name"""
        return self.database.record_by_name(domain)['city']

    def getCountryByIp(self, ip):
        """get country code"""
        return self.database.record_by_addr(ip)['country_code']

    def getCountryByDomain(self, domain):
        """get country code"""
        return self.database.record_by_name(domain)['country_code']

    def getLocationByIp(self, ip):
        """get (latitude, longitude) tuple"""
        record = self.database.record_by_addr(ip)
        return (record['latitude'], record['longitude'])

    def getLocationByDomain(self, domain):
        """get (latitude, longitude) tuple"""
        record = self.database.record_by_name(domain)
        return (record['latitude'], record['longitude'])