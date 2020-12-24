# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/utils/geoip.py
# Compiled at: 2018-07-11 18:15:30
import warnings
from django.contrib.gis import geoip
HAS_GEOIP = geoip.HAS_GEOIP
if HAS_GEOIP:
    BaseGeoIP = geoip.GeoIP
    GeoIPException = geoip.GeoIPException

    class GeoIP(BaseGeoIP):

        def __init__(self, *args, **kwargs):
            warnings.warn('GeoIP class has been moved to `django.contrib.gis.geoip`, and this shortcut will disappear in Django v1.6.', DeprecationWarning, stacklevel=2)
            super(GeoIP, self).__init__(*args, **kwargs)