# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/lead.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 209 bytes
from ovp_core import models
from rest_framework import serializers

class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
         'name', 'email', 'phone', 'country']
        model = models.Lead