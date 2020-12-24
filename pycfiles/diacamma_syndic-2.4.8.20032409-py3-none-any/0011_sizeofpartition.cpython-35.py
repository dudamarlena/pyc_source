# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0011_sizeofpartition.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1052 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
from lucterios.framework.models import LucteriosDecimalField

class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0006_depositslip_status'),
     ('condominium', '0010_exeptional_entry')]
    operations = [
     migrations.AlterField(model_name='partition', name='value', field=LucteriosDecimalField(decimal_places=2, default=0.0, max_digits=7, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100000.0)], verbose_name='tantime')),
     migrations.AlterField(model_name='propertylot', name='value', field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='tantime'))]