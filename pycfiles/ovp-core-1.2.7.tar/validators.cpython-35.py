# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/validators.py
# Compiled at: 2017-02-22 17:59:54
# Size of source mod 2**32: 715 bytes
from rest_framework import serializers
from ovp_core.serializers import GoogleAddressSerializer
from ovp_core.models import Skill
from ovp_core.models import Cause

def address_validate(address):
    address_sr = GoogleAddressSerializer(data=address)
    address_sr.is_valid(raise_exception=True)


def skill_exist(v):
    try:
        Skill.objects.get(id=v['id'])
    except Skill.DoesNotExist:
        raise serializers.ValidationError({'id': "Skill with 'id' {} does not exist.".format(v['id'])})


def cause_exist(v):
    try:
        Cause.objects.get(id=v['id'])
    except Cause.DoesNotExist:
        raise serializers.ValidationError({'id': "Cause with 'id' {} does not exist.".format(v['id'])})