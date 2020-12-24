# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0003_callfunds_expense_status.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1057 bytes
from __future__ import unicode_literals
from django.db import migrations
import django_fsm

class Migration(migrations.Migration):
    dependencies = [
     ('condominium', '0002_expensedetail_entry')]
    operations = [
     migrations.AlterField(model_name='callfunds', name='status', field=django_fsm.FSMIntegerField(choices=[(0, 'building'), (1, 'valid'), (2, 'ended')], db_index=True, default=0, verbose_name='status')),
     migrations.AlterField(model_name='expense', name='status', field=django_fsm.FSMIntegerField(choices=[(0, 'building'), (1, 'valid'), (2, 'ended')], db_index=True, default=0, verbose_name='status')),
     migrations.AlterModelOptions(name='partition', options={'default_permissions': [], 'ordering': ['owner__third_id', 'set_id'], 'verbose_name': 'partition', 'verbose_name_plural': 'partitions'})]