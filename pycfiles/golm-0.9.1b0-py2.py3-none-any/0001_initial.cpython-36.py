# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_webgui/migrations/0001_initial.py
# Compiled at: 2018-04-15 14:06:01
# Size of source mod 2**32: 2002 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name='Button',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
      (
       'text', models.CharField(max_length=255, blank=True, null=True)),
      (
       'action', models.CharField(max_length=255, blank=True, null=True)),
      (
       'url', models.CharField(max_length=1024, blank=True, null=True))]),
     migrations.CreateModel(name='Element',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
      (
       'title', models.CharField(max_length=255, blank=True, null=True)),
      (
       'subtitle', models.CharField(max_length=255, blank=True, null=True)),
      (
       'image_url', models.CharField(max_length=255, blank=True, null=True))]),
     migrations.CreateModel(name='Message',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
      (
       'text', models.CharField(max_length=255)),
      (
       'uid', models.CharField(max_length=255)),
      (
       'timestamp', models.BigIntegerField()),
      (
       'is_response', models.BooleanField(default=False))]),
     migrations.AddField(model_name='element',
       name='message',
       field=models.ForeignKey(to='golm_webgui.Message', on_delete=(models.CASCADE))),
     migrations.AddField(model_name='button',
       name='message',
       field=models.ForeignKey(to='golm_webgui.Message', on_delete=(models.CASCADE)))]