# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/db/fields.py
# Compiled at: 2016-09-04 11:39:57
# Size of source mod 2**32: 328 bytes
from django.db import models
from dyn_struct.db import validators

class ParamsField(models.TextField):

    @property
    def validators(self):
        field_validators = super(ParamsField, self).validators
        field_validators.extend([
         validators.ParamsValidator()])
        return field_validators