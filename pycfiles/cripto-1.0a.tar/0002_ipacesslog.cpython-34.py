# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/tony/B8B20CA7B20C6BE6/projects/crimson_antispam/antispam/migrations/0002_ipacesslog.py
# Compiled at: 2016-03-22 12:04:34
# Size of source mod 2**32: 803 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('antispam', '0001_initial')]
    operations = [
     migrations.CreateModel(name='IPAcessLog', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'ip_address', models.GenericIPAddressField(db_index=True, unique=True)),
      (
       'last_accessed', models.DateTimeField()),
      (
       'created_on', models.DateTimeField(auto_now_add=True)),
      (
       'updated_on', models.DateTimeField(auto_now=True))])]