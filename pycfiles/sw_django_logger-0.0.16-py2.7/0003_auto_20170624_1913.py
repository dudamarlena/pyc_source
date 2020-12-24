# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/migrations/0003_auto_20170624_1913.py
# Compiled at: 2018-02-07 05:07:39
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sw_logger', '0002_auto_20170624_1618')]
    operations = [
     migrations.RenameField(model_name=b'log', old_name=b'dc', new_name=b'created')]