# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/migrations/0002_auto_20141030_2250.py
# Compiled at: 2014-11-14 09:25:00
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('tinycms', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'page', name=b'url_overwrite', field=models.CharField(max_length=2048, null=True, blank=True))]