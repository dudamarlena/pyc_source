# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/playbook/migrations/0004_playbookrunhistory_log_url.py
# Compiled at: 2015-10-29 03:29:57
# Size of source mod 2**32: 441 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('playbook', '0003_auto_20151028_1735')]
    operations = [
     migrations.AddField(model_name='playbookrunhistory', name='log_url', field=models.CharField(default=b'', max_length=1024, blank=True))]