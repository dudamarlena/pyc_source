# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/das-g/hsr/dev/osmaxx/drf-utm-zone-info/utm_zone_info/serializers.py
# Compiled at: 2017-01-06 03:45:31
# Size of source mod 2**32: 243 bytes
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework_gis.fields import GeometryField

class GeometrySerializer(serializers.Serializer):
    geom = GeometryField()
    srid = IntegerField()