# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/sms/migrations/0002_auto_20190605_1545.py
# Compiled at: 2019-09-24 05:06:42
# Size of source mod 2**32: 307 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sms', '0001_initial')]
    operations = [
     migrations.RenameModel(old_name='Log',
       new_name='Sms')]