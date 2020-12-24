# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/playbook/migrations/0002_auto_20151028_1653.py
# Compiled at: 2015-10-28 12:53:33
# Size of source mod 2**32: 423 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('playbook', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='playbookrunhistory', name='date_finished', field=models.DateTimeField(null=True, blank=True))]