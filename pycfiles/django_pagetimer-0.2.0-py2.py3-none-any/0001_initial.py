# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-pagetimer/pagetimer/migrations/0001_initial.py
# Compiled at: 2016-05-09 12:55:08
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'PageVisit', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'username', models.TextField(default=b'anonymous')),
      (
       b'ipaddress', models.GenericIPAddressField()),
      (
       b'path', models.TextField(default=b'/')),
      (
       b'visited', models.DateTimeField(auto_now_add=True)),
      (
       b'session_key', models.TextField(default=b''))])]