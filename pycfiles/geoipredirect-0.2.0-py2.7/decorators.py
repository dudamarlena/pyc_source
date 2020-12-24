# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/decorators.py
# Compiled at: 2011-02-15 07:06:13
from geoip.middleware import GeoIPMiddleware
from django.utils.decorators import decorator_from_middleware
redirect_geoip = decorator_from_middleware(GeoIPMiddleware)