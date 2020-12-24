# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vedme/src/django-filebrowser/mediabrowser/migrations/0001_initial.py
# Compiled at: 2016-05-10 18:00:30
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Asset', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.TextField(max_length=120, verbose_name=b'name')),
      (
       b'file', models.FileField(upload_to=b'mb/%Y/%m', verbose_name=b'file')),
      (
       b'type', models.CharField(choices=[('img', 'Image'), ('doc', 'Document')], max_length=16, verbose_name=b'type')),
      (
       b'ext', models.CharField(max_length=40, verbose_name=b'type')),
      (
       b'uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name=b'uploaded on')),
      (
       b'uploaded_by', models.CharField(blank=True, max_length=80, verbose_name=b'uploaded by')),
      (
       b'width', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'width')),
      (
       b'height', models.PositiveIntegerField(blank=True, null=True, verbose_name=b'height'))])]