# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/serializers/skill.py
# Compiled at: 2017-02-22 17:59:54
# Size of source mod 2**32: 475 bytes
from ovp_core import models
from ovp_core import validators
from rest_framework import serializers

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
         'id', 'name']
        model = models.Skill


class SkillAssociationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True)

    class Meta:
        fields = [
         'id', 'name']
        model = models.Skill
        validators = [validators.skill_exist]