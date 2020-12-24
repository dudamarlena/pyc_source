# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximsmirnov/.virtualenvs/django-antivirus-field/lib/python2.7/site-packages/django_antivirus_field/fields.py
# Compiled at: 2014-10-10 08:01:32
from __future__ import unicode_literals
from django.db import models
from django_antivirus_field.validators import file_validator

class ProtectedFileField(models.FileField):

    def __init__(self, *args, **kwargs):
        super(ProtectedFileField, self).__init__(*args, **kwargs)
        self.validators.append(file_validator)