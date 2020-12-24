# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/factory.py
# Compiled at: 2018-07-11 18:15:30
from django.contrib.gis import memoryview
from django.contrib.gis.geos.geometry import GEOSGeometry, wkt_regex, hex_regex
from django.utils import six

def fromfile(file_h):
    """
    Given a string file name, returns a GEOSGeometry. The file may contain WKB,
    WKT, or HEX.
    """
    if isinstance(file_h, six.string_types):
        with open(file_h, 'rb') as (file_h):
            buf = file_h.read()
    else:
        buf = file_h.read()
    if isinstance(buf, bytes):
        try:
            decoded = buf.decode()
            if wkt_regex.match(decoded) or hex_regex.match(decoded):
                return GEOSGeometry(decoded)
        except UnicodeDecodeError:
            pass

    else:
        return GEOSGeometry(buf)
    return GEOSGeometry(memoryview(buf))


def fromstr(string, **kwargs):
    """Given a string value, returns a GEOSGeometry object."""
    return GEOSGeometry(string, **kwargs)