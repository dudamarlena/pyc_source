# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0015_calldetail.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 755 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0006_depositslip_status'),
     ('condominium', '0014_callfunds_type')]
    operations = [
     migrations.AlterModelOptions(name='callfunds', options={'ordering': ['date', 'num'], 'verbose_name': 'call of funds', 'verbose_name_plural': 'calls of funds'}),
     migrations.AlterField(model_name='calldetail', name='set', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='condominium.Set', verbose_name='set'))]