# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/simple_address.py
# Compiled at: 2017-06-20 14:52:19
# Size of source mod 2**32: 279 bytes
from ovp_core import models
from rest_framework import serializers

class SimpleAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SimpleAddress
        fields = ['street', 'number', 'neighbourhood', 'city', 'state', 'zipcode', 'country', 'supplement']