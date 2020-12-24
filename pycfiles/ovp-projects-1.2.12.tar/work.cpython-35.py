# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/serializers/work.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 294 bytes
from ovp_projects import models
from rest_framework import serializers

class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Work
        fields = ['weekly_hours', 'description', 'project', 'can_be_done_remotely']
        extra_kwargs = {'project': {'write_only': True}}