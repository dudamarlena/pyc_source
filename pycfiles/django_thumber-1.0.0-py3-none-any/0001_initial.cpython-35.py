# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/theukdave/Library/Mobile Documents/com~apple~CloudDocs/Sites/dit-thumber/thumber/migrations/0001_initial.py
# Compiled at: 2017-02-28 06:23:26
# Size of source mod 2**32: 1001 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='ContentFeedback', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now=True)),
      (
       'satisfied', models.BooleanField()),
      (
       'comment', models.TextField(blank=True, null=True)),
      (
       'url', models.URLField()),
      (
       'view_name', models.CharField(max_length=255)),
      (
       'utm_params', models.TextField(null=True)),
      (
       'session', models.CharField(max_length=64))], options={'ordering': ('-created', )})]