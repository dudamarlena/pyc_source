# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0011_auto_20170626_1616.py
# Compiled at: 2017-06-26 16:16:04
# Size of source mod 2**32: 437 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0010_auto_20170626_1509')]
    operations = [
     migrations.RenameField(model_name='resource', old_name='created', new_name='registered')]