# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/tony/B8B20CA7B20C6BE6/projects/crimson_antispam/antispam/migrations/0001_initial.py
# Compiled at: 2016-03-19 06:26:51
# Size of source mod 2**32: 722 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='SpamIP', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'ip_address', models.GenericIPAddressField(db_index=True, unique=True)),
      (
       'created_on', models.DateTimeField(auto_now_add=True)),
      (
       'updated_on', models.DateTimeField(auto_now=True))])]