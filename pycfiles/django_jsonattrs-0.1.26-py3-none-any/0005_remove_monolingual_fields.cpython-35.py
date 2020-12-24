# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0005_remove_monolingual_fields.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 520 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('jsonattrs', '0004_convert_multilingual_fields')]
    operations = [
     migrations.RemoveField(model_name='attribute', name='choice_labels'),
     migrations.RemoveField(model_name='attribute', name='long_name')]