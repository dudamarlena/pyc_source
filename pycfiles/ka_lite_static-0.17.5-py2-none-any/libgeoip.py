# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geoip/libgeoip.py
# Compiled at: 2018-07-11 18:15:30
import os
from ctypes import CDLL
from ctypes.util import find_library
from django.conf import settings
GEOIP_SETTINGS = dict((key, getattr(settings, key)) for key in ('GEOIP_PATH', 'GEOIP_LIBRARY_PATH',
                                                                'GEOIP_COUNTRY',
                                                                'GEOIP_CITY') if hasattr(settings, key))
lib_path = GEOIP_SETTINGS.get('GEOIP_LIBRARY_PATH', None)
if lib_path:
    lib_name = None
else:
    lib_name = 'GeoIP'
if lib_name:
    lib_path = find_library(lib_name)
if lib_path is None:
    raise GeoIPException('Could not find the GeoIP library (tried "%s"). Try setting GEOIP_LIBRARY_PATH in your settings.' % lib_name)
lgeoip = CDLL(lib_path)
if os.name == 'nt':
    libc = CDLL('msvcrt')
else:
    libc = CDLL(None)
free = libc.free