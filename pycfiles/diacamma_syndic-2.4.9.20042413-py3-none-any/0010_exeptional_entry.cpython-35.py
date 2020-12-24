# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0010_exeptional_entry.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1389 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0006_depositslip_status'),
     ('accounting', '0004_modelentry_costaccounting'),
     ('condominium', '0009_setcost')]
    operations = [
     migrations.CreateModel(name='PartitionExceptional', fields=[], options={'verbose_name': 'exceptional class load', 
      'verbose_name_plural': 'exceptional class loads', 
      'proxy': True, 
      'ordering': ['owner__third_id', 'set_id'], 
      'default_permissions': []}, bases=('condominium.partition', )),
     migrations.AddField(model_name='calldetail', name='entry', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.EntryAccount', verbose_name='entry')),
     migrations.AlterField(model_name='expensedetail', name='entry', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.EntryAccount', verbose_name='entry'))]