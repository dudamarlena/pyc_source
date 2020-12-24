# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/tests/serializers.py
from datapunt_api.rest import HALSerializer
from rest_framework import serializers
from tests import models

class WeatherStationSerializer(HALSerializer):

    class Meta:
        model = models.WeatherStation
        fields = '__all__'


class WeatherDetailStationSerializer(HALSerializer):
    detailed = serializers.SerializerMethodField()

    class Meta:
        model = models.WeatherStation
        fields = [
         '_links',
         'number',
         'detailed']

    def get_detailed(self, obj):
        return 'I am detailed'


class TemperatureRecordSerializer(HALSerializer):

    class Meta:
        model = models.TemperatureRecord
        fields = '__all__'