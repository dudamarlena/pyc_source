# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/serializers.py
# Compiled at: 2017-04-21 22:16:24
# Size of source mod 2**32: 795 bytes
from google_address import models
try:
    from rest_framework import serializers
except ImportError:
    print('You need djangorestframework to use google_address.serializers')
else:

    class AddressSerializer(serializers.ModelSerializer):

        class Meta:
            model = models.Address
            fields = ['raw', 'raw2', 'address_line', 'city_state']
            read_only_fields = ['address_line', 'city_state']


    class AddressLatLngSerializer(serializers.ModelSerializer):

        class Meta:
            model = models.Address
            fields = ['raw', 'raw2', 'address_line', 'city_state', 'lat', 'lng']
            read_only_fields = ['address_line', 'city_state', 'lat', 'lng']


    class AddressCityStateSerializer(serializers.ModelSerializer):

        class Meta:
            model = models.Address
            fields = ['city_state']