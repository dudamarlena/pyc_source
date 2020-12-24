# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0005_auto_20170624_0943.py
# Compiled at: 2017-06-24 09:43:15
# Size of source mod 2**32: 428 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0004_auto_20170624_0941')]
    operations = [
     migrations.RenameField(model_name='resource', old_name='uuid', new_name='name')]