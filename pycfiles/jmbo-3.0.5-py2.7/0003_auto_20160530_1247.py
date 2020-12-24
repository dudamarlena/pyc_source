# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0003_auto_20160530_1247.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0002_auto_20160530_1338')]
    operations = [
     migrations.AlterModelOptions(name=b'modelbaseimage', options={b'ordering': ('position', )}),
     migrations.RemoveField(model_name=b'modelbase', name=b'crop_from'),
     migrations.RemoveField(model_name=b'modelbase', name=b'date_taken'),
     migrations.RemoveField(model_name=b'modelbase', name=b'effect'),
     migrations.RemoveField(model_name=b'modelbase', name=b'image'),
     migrations.RemoveField(model_name=b'modelbase', name=b'view_count')]