# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0008_auto_20190308_1642.py
# Compiled at: 2019-07-02 16:47:10
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explorer', '0007_querylog_connection')]
    operations = [
     migrations.AlterField(model_name=b'query', name=b'connection', field=models.CharField(blank=True, help_text=b'Name of DB connection (as specified in settings) to use for this query. Will use EXPLORER_DEFAULT_CONNECTION if left blank', max_length=128, null=True))]