# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/tests/views.py
"""Test views."""
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datapunt_api.rest import DatapuntViewSet
from datapunt_api import bbox
from tests.models import WeatherStation
from tests.models import TemperatureRecord
from tests.serializers import WeatherStationSerializer
from tests.serializers import WeatherDetailStationSerializer
from tests.serializers import TemperatureRecordSerializer

class WeatherFilter(FilterSet):
    __doc__ = 'Weather station fitler.\n\n    test geo location filtering\n    '
    location = filters.CharFilter(method='locatie_filter',
      label='x,y,r')
    location_rd = filters.CharFilter(method='locatie_filter_rd',
      label='x,y,r')

    def locatie_filter(self, qs, name, value):
        point, radius = bbox.parse_xyr(value)
        return qs.filter(centroid__geometrie__dwithin=(
         point, radius))

    def locatie_filter_rd(self, qs, name, value):
        point, radius = bbox.parse_xyr(value, srid=28992)
        return qs.filter(centroid_rd__dwithin=(
         point, radius))

    class Meta(object):
        model = WeatherStation
        fields = ('location', 'location_rd')


class WeatherStationViewSet(DatapuntViewSet):
    serializer_class = WeatherStationSerializer
    serializer_detail_class = WeatherDetailStationSerializer
    queryset = WeatherStation.objects.all().order_by('id')
    filter_class = WeatherFilter
    filter_backends = (
     DjangoFilterBackend,
     OrderingFilter)
    ordering_fields = '__all__'


class TemperatureRecordViewSet(DatapuntViewSet):
    serializer_class = TemperatureRecordSerializer
    serializer_detail_class = TemperatureRecordSerializer
    queryset = TemperatureRecord.objects.all().order_by('date')

    def list(self, request, *args, **kwargs):
        return (super().list)(self, request, *args, **kwargs)