# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0013_auto_20181130_1346.py
# Compiled at: 2018-11-30 00:46:47
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0012_auto_20181129_1444')]
    operations = [
     migrations.AlterModelOptions(name=b'mission', options={b'ordering': [b'created_at']})]