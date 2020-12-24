# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/migrations/0001_initial.py
# Compiled at: 2018-03-01 05:20:53
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'ThemaCategory', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'code', models.CharField(max_length=100, unique=True)),
      (
       b'header', models.TextField()),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'thema.ThemaCategory'))], options={b'ordering': ('updated_at', )})]