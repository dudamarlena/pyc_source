# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Cycloid/Cyclosible/cyclosible/appversion/migrations/0001_initial.py
# Compiled at: 2015-12-09 09:44:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('playbook', '0007_auto_20151209_1444')]
    operations = [
     migrations.CreateModel(name=b'AppVersion', fields=[
      (
       b'id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name=b'ID')),
      (
       b'application', models.CharField(max_length=100, unique=True)),
      (
       b'version', models.CharField(max_length=128, default=b'')),
      (
       b'env', models.CharField(max_length=10, choices=[('PROD', 'prod'), ('PREPROD', 'preprod'), ('DEV', 'dev'), ('INFRA', 'infra')], default=b'PROD')),
      (
       b'deployed', models.BooleanField(default=False)),
      (
       b'playbook', models.ForeignKey(to=b'playbook.Playbook'))])]