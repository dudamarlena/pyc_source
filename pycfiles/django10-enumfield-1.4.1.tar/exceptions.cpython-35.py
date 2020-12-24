# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jb/projects/i2biz/misc/django-enumfield/django_enumfield/exceptions.py
# Compiled at: 2017-10-06 05:18:16
# Size of source mod 2**32: 114 bytes
from django.core.exceptions import ValidationError

class InvalidStatusOperationError(ValidationError):
    pass