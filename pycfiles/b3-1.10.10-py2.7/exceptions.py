# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\geolocation\exceptions.py
# Compiled at: 2016-03-08 18:42:10


class GeolocalizationError(Exception):
    """
    Raised when we are not able to geolocalize an IP address
    """

    def __init__(self, message):
        Exception.__init__(self, message)

    def __str__(self):
        return repr(self.message)