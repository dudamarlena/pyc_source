# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/playbook/migrations/0007_auto_20151209_1444.py
# Compiled at: 2015-12-09 09:44:29
# Size of source mod 2**32: 431 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('playbook', '0006_auto_20151105_0618')]
    operations = [
     migrations.AlterField(model_name='playbook', name='subset', field=models.CharField(max_length=1024, blank=True, default=''))]