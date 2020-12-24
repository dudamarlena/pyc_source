# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kubus/workspace/django-dbtemplate/dbtemplate/migrations/0001_initial.py
# Compiled at: 2015-06-08 01:34:17
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Template', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug',
       models.CharField(unique=True, max_length=255, verbose_name=b'slug')),
      (
       b'data',
       models.TextField(verbose_name=b'content')),
      (
       b'specs',
       models.TextField(default=b'', verbose_name=b'specification'))], options={b'verbose_name': b'template', 
        b'verbose_name_plural': b'templates'})]