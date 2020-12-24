# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/exceptions.py
# Compiled at: 2011-01-24 12:29:55


class NoGeoIPException(Exception):
    pass


class InvalidDottedIP(Exception):
    pass


class NoGeoRedirectFound(Exception):
    pass