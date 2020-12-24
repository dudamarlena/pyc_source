# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\geolocation\location.py
# Compiled at: 2016-03-08 18:42:10
import unicodedata

class Location(object):

    def __init__(self, country=None, region=None, city=None, cc=None, rc=None, isp=None, lat=None, lon=None, timezone=None, zipcode=None):
        """
        :param country: The country name
        :param region: The regione name
        :param city: The city name
        :param cc: The country code
        :param rc: The region code
        :param isp: The ISP name
        :param lat: The latitude value
        :param lon: The longitude value
        :param timezone: The timezone value (long string)
        :param zipcode; The zipcode value
        """
        self.country = country or None
        self.region = region or None
        self.city = city or None
        self.cc = cc or None
        self.rc = rc or None
        self.isp = isp or None
        self.lat = lat or None
        self.lon = lon or None
        self.timezone = timezone or None
        self.zipcode = zipcode or None
        return

    def __setattr__(self, key, value):
        """
        Proxy which cleanup attribute value before assignment,
        :param key: The attribute name
        :param value: The attribute value
        """
        if value:
            value = unicodedata.normalize('NFKD', unicode(value)).encode('ascii', 'ignore').strip()
        self.__dict__[key] = value

    def __repr__(self):
        """
        Object representation,
        :return: string
        """
        v = [ '%s=%s' % (x, getattr(self, x)) for x in dir(self) if not x.startswith('__') and not callable(getattr(self, x)) ]
        return 'Location<%s>' % (', ').join(v)