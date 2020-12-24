# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0009_setcost.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1417 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0006_depositslip_status'),
     ('accounting', '0004_modelentry_costaccounting'),
     ('condominium', '0008_callfunds_type')]
    operations = [
     migrations.CreateModel(name='SetCost', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'cost_accounting', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.CostAccounting', verbose_name='cost accounting')),
      (
       'set', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='condominium.Set', verbose_name='class load')),
      (
       'year', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.FiscalYear', verbose_name='fiscal year'))], options={'verbose_name': 'cost of class load', 
      'default_permissions': [], 
      'verbose_name_plural': 'costs of class load', 
      'ordering': ['year_id', 'set_id']})]