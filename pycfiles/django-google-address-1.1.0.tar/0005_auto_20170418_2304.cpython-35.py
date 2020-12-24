# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/migrations/0005_auto_20170418_2304.py
# Compiled at: 2017-04-18 19:04:36
# Size of source mod 2**32: 408 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('google_address', '0004_auto_20170418_0133')]
    operations = [
     migrations.RenameModel(old_name='GoogleAddress', new_name='Address')]