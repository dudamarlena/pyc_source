# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/event/migrations/0005_invoice_change.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 927 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('event', '0004_event_status')]
    operations = [
     migrations.AddField(model_name='participant', name='reduce', field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(9999999.999)], verbose_name='reduce')),
     migrations.AddField(model_name='event', name='cost_accounting', field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.CostAccounting', verbose_name='cost accounting'))]