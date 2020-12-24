# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0009_auto_20150317_1324.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0008_auto_20150317_0450')]
    operations = [
     migrations.RenameField(model_name=b'message', old_name=b'reties', new_name=b'retries')]