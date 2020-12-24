# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/fields.py
# Compiled at: 2018-11-05 07:19:14
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class PhoneField(models.CharField):

    def __init__(self, max_length=255, validators=[], mobile=False, *args, **kwargs):
        if mobile:
            validators = [RegexValidator(regex='^0{2}[1-9]{1}[0-9]{0,2}[1-9][0-9]{2}[0-9]{3}[0-9]{4}$')]
        else:
            validators = [
             RegexValidator(regex='^0(?!0)\\d{2}([0-9]{8})$', message=_('phone is not valid, please insert with code'), code='nomatch')]
        super(PhoneField, self).__init__(max_length=max_length, validators=validators, *args, **kwargs)


class PriceField(models.DecimalField):

    def __init__(self, big=False, max_digits=8, decimal_places=0, *args, **kwargs):
        if big:
            max_digits = 20
        super(PriceField, self).__init__(max_digits=max_digits, decimal_places=decimal_places, *args, **kwargs)


class NationalCodeField(models.CharField):

    def __init__(self, validators=[], max_length=10, birth_certificate=False, *args, **kwargs):
        validators = []
        if birth_certificate:
            validators = [RegexValidator(regex='^\\d{1,10}$', message=_('Birth Certificate code is not valide'), code='nomatch')]
        else:
            validators = [
             RegexValidator(regex='^\\d{10}$', message=_('National Code is not valide'), code='nomatch')]
        super(NationalCodeField, self).__init__(max_length=max_length, validators=validators, *args, **kwargs)


class PostalCodeField(models.CharField):

    def __init__(self, max_length=10, validators=[], *args, **kwargs):
        validators = [RegexValidator(regex='^\\d{10}$', message=_('zip code is not valid'), code='nomatch')]
        super(PostalCodeField, self).__init__(max_length=max_length, validators=validators, *args, **kwargs)