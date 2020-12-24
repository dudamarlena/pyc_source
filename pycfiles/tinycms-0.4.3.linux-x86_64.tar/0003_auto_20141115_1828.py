# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/migrations/0003_auto_20141115_1828.py
# Compiled at: 2014-11-22 22:14:04
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('tinycms', '0002_auto_20141030_2250')]
    operations = [
     migrations.AlterField(model_name=b'page', name=b'template', field=models.CharField(max_length=1024, choices=[('test_template.html', 'test_template')]))]