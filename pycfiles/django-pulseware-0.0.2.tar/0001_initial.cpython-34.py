# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/sf3/lib/python3.4/site-packages/pulseware/migrations/0001_initial.py
# Compiled at: 2016-01-18 12:22:54
# Size of source mod 2**32: 562 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Heartbeat', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'updated_at', models.DateTimeField(auto_now=True))])]