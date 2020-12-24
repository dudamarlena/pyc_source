# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/migrations/0004_auto_20141117_2225.py
# Compiled at: 2014-11-22 22:14:04
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('tinycms', '0003_auto_20141115_1828')]
    operations = [
     migrations.AlterField(model_name=b'content', name=b'content', field=models.TextField(default=b''))]