# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/decorators.py
# Compiled at: 2018-02-16 03:21:13
# Size of source mod 2**32: 281 bytes
from django.db.models.signals import post_init, pre_save
from .signals import fixup_instance, attribute_model_pre_save

def fix_model_for_attributes(cls):
    post_init.connect(fixup_instance, sender=cls)
    pre_save.connect(attribute_model_pre_save, sender=cls)
    return cls