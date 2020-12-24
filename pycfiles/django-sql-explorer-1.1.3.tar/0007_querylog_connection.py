# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0007_querylog_connection.py
# Compiled at: 2019-07-02 16:47:10
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('explorer', '0006_query_connection')]
    operations = [
     migrations.AddField(model_name=b'querylog', name=b'connection', field=models.CharField(max_length=128, null=True, blank=True))]