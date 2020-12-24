# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\geolocator\config.py
# Compiled at: 2006-03-06 15:28:24
"""

 To use the data providers, thus getting access to the location and/or geoip
 data, data providers have to be selected.

 In the long run, we want to make provider selection at least semi-automatic.
 For now, however, the providers have to be manually configured here.

 Since we don't yet have a windows binary to distribute with the library,
 we default to DummyProvider.

 If you're on unix, use the MaxMindCountryIpProvider.
 If you've purchased the MaxMind GeoIP City database,
 use MaxMindCityIpProvider.

"""
from providers import DummyProvider
from providers import MaxMindCountryDataProvider
from providers import MaxMindCityDataProvider
MAXMINDLOCATIONS = ('./data', '/usr/share/GeoIP', '/usr/local/share/GeoIP')
DEFAULTPROVIDER = DummyProvider