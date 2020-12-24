# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/migrations/0003_auto_20170417_2356.py
# Compiled at: 2017-04-17 19:56:39
# Size of source mod 2**32: 444 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('google_address', '0002_auto_20170417_2307')]
    operations = [
     migrations.RenameField(model_name='googleaddress', old_name='typed_address', new_name='raw')]