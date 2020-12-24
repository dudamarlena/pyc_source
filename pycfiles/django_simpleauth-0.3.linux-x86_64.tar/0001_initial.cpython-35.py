# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratheek/msc/pythons/lib/python3.5/site-packages/simpleauth/migrations/0001_initial.py
# Compiled at: 2017-02-09 05:20:29
# Size of source mod 2**32: 616 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Users', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'username', models.CharField(max_length=15)),
      (
       'password', models.CharField(max_length=15))])]