# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/google_address.py
# Compiled at: 2017-04-20 14:47:52
# Size of source mod 2**32: 719 bytes
from ovp_core import models
from rest_framework import serializers

class GoogleAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GoogleAddress
        fields = ['typed_address', 'typed_address2', 'address_line', 'city_state']
        read_only_fields = ['address_line', 'city_state']


class GoogleAddressLatLngSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GoogleAddress
        fields = ['typed_address', 'typed_address2', 'address_line', 'city_state', 'lat', 'lng']
        read_only_fields = ['address_line', 'city_state']


class GoogleAddressCityStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GoogleAddress
        fields = ['city_state']