# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0017_auto_20170404_0730.py
# Compiled at: 2017-08-17 00:05:08
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0016_auto_20161004_0543')]
    operations = [
     migrations.AlterField(model_name=b'partner', name=b'mdn', field=models.BooleanField(default=False, verbose_name=b'Request MDN'))]