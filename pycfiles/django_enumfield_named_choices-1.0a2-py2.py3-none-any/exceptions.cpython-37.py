# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /pmc/Work/kolotev/0git/.github/django-enumfield-named-choices/django_enumfield_named_choices/exceptions.py
# Compiled at: 2019-08-20 18:04:03
# Size of source mod 2**32: 114 bytes
from django.core.exceptions import ValidationError

class InvalidStatusOperationError(ValidationError):
    pass