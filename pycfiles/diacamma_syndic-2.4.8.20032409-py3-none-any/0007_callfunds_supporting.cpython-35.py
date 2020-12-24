# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0007_callfunds_supporting.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1114 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0006_depositslip_status'),
     ('condominium', '0006_expenseratio')]
    operations = [
     migrations.CreateModel(name='CallFundsSupporting', fields=[], options={'default_permissions': []}, bases=('payoff.supporting', )),
     migrations.AlterModelOptions(name='partition', options={'default_permissions': [], 'ordering': ['owner__third_id', 'set_id'], 
      'verbose_name': 'division', 'verbose_name_plural': 'divisions'}),
     migrations.AddField(model_name='callfunds', name='supporting', field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='condominium.CallFundsSupporting'))]