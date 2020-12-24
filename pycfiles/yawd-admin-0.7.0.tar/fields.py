# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/elorus/local/lib/python2.7/site-packages/yawdadmin/fields.py
# Compiled at: 2013-08-25 05:42:06
import re
from django.db import models
from django.core.exceptions import ValidationError

class OptionNameField(models.CharField):

    def clean(self, value):
        value = super(OptionNameField, self).clean(value)
        if not re.match('[a-zA-Z_]+', value):
            raise ValidationError('Only letters and underscores are allowed.')
        return value