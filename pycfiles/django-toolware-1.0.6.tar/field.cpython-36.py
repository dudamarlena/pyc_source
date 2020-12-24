# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/utils/field.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 330 bytes
from django.db import models

class EmailFieldLowerCase(models.EmailField):
    __doc__ = 'Case-Insensitive Email (lower case)'

    def get_prep_value(self, value):
        prep_value = super(EmailFieldLowerCase, self).get_prep_value(value)
        if prep_value:
            prep_value = prep_value.lower()
        return prep_value