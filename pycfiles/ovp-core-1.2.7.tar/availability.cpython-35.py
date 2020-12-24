# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/availability.py
# Compiled at: 2017-06-13 14:16:15
# Size of source mod 2**32: 572 bytes
from ovp_core import validators
from ovp_core.models import Availability
from rest_framework import serializers

class AvailabilitySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {'weekday': instance.weekday, 'period': instance.period}

    def validate(self, data):
        if 'period_index' not in data:
            data['period_index'] = Availability.compose_period_index_for(data.get('weekday', 0), data.get('period', 0))
        return super().validate(data)

    class Meta:
        fields = [
         'weekday', 'period']
        model = Availability