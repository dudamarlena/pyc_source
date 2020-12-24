# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/DATA-LINUX/Cycloid/Cyclosible/cyclosible/playbook/migrations/0005_auto_20151102_0655.py
# Compiled at: 2015-11-02 05:36:24
# Size of source mod 2**32: 1750 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('playbook', '0004_playbookrunhistory_log_url')]
    operations = [
     migrations.AlterModelOptions(name='playbook', options={'permissions': (('view_playbook', 'Can view the playbook'), ('can_override_skip_tags', 'Can override skip_tags'),
 ('can_override_only_tags', 'Can override only_tags'), ('can_override_extra_vars', 'Can override extra_vars'),
 ('can_run_playbook', 'Can run the playbook'))}),
     migrations.AddField(model_name='playbook', name='extra_vars', field=models.CharField(default='', max_length=1024, blank=True)),
     migrations.AlterField(model_name='playbook', name='only_tags', field=models.CharField(default='', max_length=1024, blank=True)),
     migrations.AlterField(model_name='playbook', name='skip_tags', field=models.CharField(default='', max_length=1024, blank=True)),
     migrations.AlterField(model_name='playbookrunhistory', name='log_url', field=models.CharField(default='', max_length=1024, blank=True)),
     migrations.AlterField(model_name='playbookrunhistory', name='status', field=models.CharField(default='RUNNING', max_length=1024)),
     migrations.AlterField(model_name='playbookrunhistory', name='task_id', field=models.CharField(default='', max_length=1024, blank=True))]