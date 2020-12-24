# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/geopy/geocoders/dot_us.py
# Compiled at: 2013-10-14 11:27:57
import getpass
from urllib import urlencode
from urllib2 import urlopen
from geopy.geocoders.base import Geocoder
from geopy import util
import csv

class GeocoderDotUS(Geocoder):

    def __init__(self, username=None, password=None, format_string='%s'):
        if username and password is None:
            password = getpass.getpass('geocoder.us password for %r: ' % username)
        self.format_string = format_string
        self.username = username
        self.__password = password
        return

    def get_url(self):
        username = self.username
        password = self.__password
        if username and password:
            auth = '%s@%s:' % (username, password)
            resource = 'member/service/namedcsv'
        else:
            auth = ''
            resource = 'service/namedcsv'
        return 'http://%sgeocoder.us/%s' % (auth, resource)

    def geocode(self, query, exactly_one=True):
        if isinstance(query, unicode):
            query = query.encode('utf-8')
        query_str = self.format_string % query
        page = urlopen('%s?%s' % (
         self.get_url(),
         urlencode({'address': query_str})))
        reader = csv.reader(page)
        places = [ r for r in reader ]
        return self._parse_result(places[0])

    @staticmethod
    def _parse_result(result):
        place = dict(filter(lambda x: len(x) > 1, map(lambda x: x.split('=', 1), result)))
        address = [
         place.get('number', None),
         place.get('prefix', None),
         place.get('street', None),
         place.get('type', None),
         place.get('suffix', None)]
        city = place.get('city', None)
        state = place.get('state', None)
        zip_code = place.get('zip', None)
        name = util.join_filter(', ', [
         util.join_filter(' ', address),
         city,
         util.join_filter(' ', [state, zip_code])])
        latitude = place.get('lat', None)
        longitude = place.get('long', None)
        if latitude and longitude:
            latlon = (
             float(latitude), float(longitude))
        else:
            return
        return (
         name, latlon)