# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/serializers.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 2196 bytes
from rest_framework import serializers
from .models import CartoDBTable, GatewayType, Location, LocationRemapHistory

class CartoDBTableSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = CartoDBTable
        fields = ('id', 'domain', 'api_key', 'table_name', 'display_name', 'pcode_col',
                  'color', 'location_type', 'name_col')


class GatewayTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GatewayType
        fields = '__all__'


class LocationLightSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.SerializerMethodField()
    gateway = GatewayTypeSerializer()

    @staticmethod
    def get_name(obj):
        return '{} [{} - {}]'.format(obj.name, obj.gateway.name, obj.p_code)

    class Meta:
        model = Location
        fields = ('id', 'name', 'p_code', 'gateway')


class LocationSerializer(LocationLightSerializer):
    geo_point = serializers.StringRelatedField()

    class Meta(LocationLightSerializer.Meta):
        model = Location
        fields = LocationLightSerializer.Meta.fields + ('geo_point', 'parent')


class LocationExportSerializer(serializers.ModelSerializer):
    location_type = serializers.CharField(source='gateway.name')
    geo_point = serializers.StringRelatedField()
    point = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = '__all__'


class LocationExportFlatSerializer(serializers.ModelSerializer):
    location_type = serializers.CharField(source='gateway.name')
    geom = serializers.SerializerMethodField()
    point = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = '__all__'

    def get_geom(self, obj):
        if obj.geom:
            return obj.geom.point_on_surface
        else:
            return ''


class LocationRemapHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationRemapHistory
        fields = '__all__'