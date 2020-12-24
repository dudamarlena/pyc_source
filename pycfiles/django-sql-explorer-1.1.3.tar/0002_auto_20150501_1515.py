# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0002_auto_20150501_1515.py
# Compiled at: 2019-07-02 16:47:10
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('explorer', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name=b'querylog', name=b'is_playground'),
     migrations.AlterField(model_name=b'querylog', name=b'sql', field=models.TextField(null=True, blank=True))]