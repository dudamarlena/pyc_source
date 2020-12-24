# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximsmirnov/.virtualenvs/django-antivirus-field/lib/python2.7/site-packages/django_antivirus_field/validators.py
# Compiled at: 2014-10-10 08:01:32
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_antivirus_field.utils import is_infected

def file_validator(f):
    has_virus, name = is_infected(f.file.read())
    if has_virus:
        raise ValidationError(_(b'Virus "{}" was detected').format(name))