# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/migrations/0003_auto_20171124_1049.py
# Compiled at: 2018-05-10 08:40:57
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('link', '0002_auto_20160902_0249')]
    operations = [
     migrations.AlterModelOptions(name=b'viewparam', options={b'ordering': [b'key']})]