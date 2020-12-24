# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/migrations/0002_auto_20161219_1041.py
# Compiled at: 2018-03-27 03:51:51
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('layers', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'layer', options={b'ordering': ('name', )})]