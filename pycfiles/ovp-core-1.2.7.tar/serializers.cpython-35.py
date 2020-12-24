# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/serializers.py
# Compiled at: 2017-04-20 14:47:18
# Size of source mod 2**32: 1168 bytes
from ovp_core import models
from rest_framework import serializers

class EmptySerializer(serializers.Serializer):

    class Meta:
        fields = []


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


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
         'name']
        model = models.Skill


class CauseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
         'name']
        model = models.Cause


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
         'name', 'email', 'phone', 'country']
        model = models.Lead