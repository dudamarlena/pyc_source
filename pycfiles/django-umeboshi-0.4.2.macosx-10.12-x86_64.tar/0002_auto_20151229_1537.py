# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/migrations/0002_auto_20151229_1537.py
# Compiled at: 2015-12-31 08:37:33
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('umeboshi', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'event', name=b'data_pickled', field=models.BinaryField(blank=True))]