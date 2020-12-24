# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/snappion_backend/avishan/migrations/0006_auto_20200219_0421.py
# Compiled at: 2020-02-18 19:51:47
# Size of source mod 2**32: 812 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0005_baseuser_language')]
    operations = [
     migrations.RemoveField(model_name='email',
       name='is_verified'),
     migrations.RemoveField(model_name='phone',
       name='is_verified'),
     migrations.AddField(model_name='email',
       name='date_verified',
       field=models.DateTimeField(blank=True, default=None, null=True)),
     migrations.AddField(model_name='phone',
       name='date_verified',
       field=models.DateTimeField(blank=True, default=None, null=True))]