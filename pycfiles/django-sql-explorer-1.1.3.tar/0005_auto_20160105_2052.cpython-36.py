# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0005_auto_20160105_2052.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 503 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explorer', '0004_querylog_duration')]
    operations = [
     migrations.AlterField(model_name='query',
       name='snapshot',
       field=models.BooleanField(default=False, help_text='Include in snapshot task (if enabled)'))]