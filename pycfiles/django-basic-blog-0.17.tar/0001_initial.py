# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/migrations/0001_initial.py
# Compiled at: 2015-07-14 12:37:49
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Entry', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=200)),
      (
       b'content', models.TextField())], options={}, bases=(
      models.Model,))]