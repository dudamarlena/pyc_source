# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/validators.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 495 bytes
from rest_framework import serializers
from ovp_users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def invite_email_validator(email):
    try:
        validate_email(email)
    except ValidationError as e:
        return True

    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError('This user is not valid.')