# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/fields.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2245 bytes
from django.db import models
from django.core.validators import RegexValidator
import django.utils.translation as _

class PhoneField(models.CharField):

    def __init__(self, max_length=255, validators=[], mobile=False, *args, **kwargs):
        if mobile:
            validators = [RegexValidator(regex='^0{2}[1-9]{1}[0-9]{0,2}[1-9][0-9]{2}[0-9]{3}[0-9]+$')]
        else:
            validators = [
             RegexValidator(regex='^0(?!0)\\d{2}([0-9]{8})$', message=(_('phone is not valid, please insert with code')), code='nomatch')]
        (super(PhoneField, self).__init__)(args, max_length=max_length, validators=validators, **kwargs)


class PriceField(models.DecimalField):

    def __init__(self, big=False, max_digits=8, decimal_places=0, *args, **kwargs):
        if big:
            max_digits = 20
        (super(PriceField, self).__init__)(args, max_digits=max_digits, decimal_places=decimal_places, **kwargs)


class NationalCodeField(models.CharField):

    def __init__(self, validators=[], max_length=10, birth_certificate=False, *args, **kwargs):
        validators = []
        if birth_certificate:
            validators = [RegexValidator(regex='^\\d{1,10}$', message=(_('Birth Certificate code is not valide')), code='nomatch')]
        else:
            validators = [
             RegexValidator(regex='^\\d{10}$', message=(_('National Code is not valide')), code='nomatch')]
        (super(NationalCodeField, self).__init__)(args, max_length=max_length, validators=validators, **kwargs)


class PostalCodeField(models.CharField):

    def __init__(self, max_length=10, validators=[], *args, **kwargs):
        validators = [RegexValidator(regex='^\\d{10}$', message=(_('zip code is not valid')), code='nomatch')]
        (super(PostalCodeField, self).__init__)(args, max_length=max_length, validators=validators, **kwargs)