# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cities_tiny/settings.py
# Compiled at: 2012-03-14 13:44:03
from django.conf import settings
COUNTRY_SOURCES = getattr(settings, 'CITIES_TINY_COUNTRY_SOURCES', [
 'http://download.geonames.org/export/dump/countryInfo.txt'])
ADMIN_SOURCES = getattr(settings, 'CITIES_TINY_ADMIN_SOURCES', [
 'http://download.geonames.org/export/dump/admin1CodesASCII.txt',
 'http://download.geonames.org/export/dump/admin2Codes.txt'])
CITY_SOURCES = getattr(settings, 'CITIES_TINY_CITY_SOURCES', [
 'http://download.geonames.org/export/dump/cities15000.zip'])
ALTERNATE_NAMES = getattr(settings, 'CITIES_TINY_ALTERNATE_NAMES', [
 'http://download.geonames.org/export/dump/alternateNames.zip'])
ENABLE_I18N = getattr(settings, 'CITIES_TINY_ENABLE_I18N', True)
LANGUAGES = getattr(settings, 'CITIES_TINY_LANGUAGES', [
 settings.LANGUAGE_CODE[:2],
 'like-' + settings.LANGUAGE_CODE[:2]])
COUNTRIES = getattr(settings, 'CITIES_TINY_COUNTRIES', None)
CITY_MIN_POPULATION = getattr(settings, 'CITIES_TINY_CITY_MIN_POPULATION', 15000)
ADMIN_MAX_LEVEL = getattr(settings, 'CITIES_TINY_ADMIN_MIN_LEVEL', 2)
DATA_DIR = getattr(settings, 'CITIES_TINY_DATA_DIR', 'data')