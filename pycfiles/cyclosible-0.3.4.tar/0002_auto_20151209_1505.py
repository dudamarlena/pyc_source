# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/appversion/migrations/0002_auto_20151209_1505.py
# Compiled at: 2015-12-09 10:05:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('appversion', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'appversion', name=b'application', field=models.CharField(max_length=100)),
     migrations.AlterField(model_name=b'appversion', name=b'version', field=models.CharField(max_length=128))]