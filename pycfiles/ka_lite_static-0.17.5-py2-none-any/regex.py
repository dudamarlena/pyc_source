# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geometry/regex.py
# Compiled at: 2018-07-11 18:15:30
import re
hex_regex = re.compile('^[0-9A-F]+$', re.I)
wkt_regex = re.compile('^(SRID=(?P<srid>\\-?\\d+);)?(?P<wkt>(?P<type>POINT|LINESTRING|LINEARRING|POLYGON|MULTIPOINT|MULTILINESTRING|MULTIPOLYGON|GEOMETRYCOLLECTION)[ACEGIMLONPSRUTYZ\\d,\\.\\-\\(\\) ]+)$', re.I)
json_regex = re.compile('^(\\s+)?\\{[\\s\\w,\\[\\]\\{\\}\\-\\."\\\':]+\\}(\\s+)?$')