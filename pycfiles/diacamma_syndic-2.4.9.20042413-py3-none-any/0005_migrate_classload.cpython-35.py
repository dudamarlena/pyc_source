# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0005_migrate_classload.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1119 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('condominium', '0004_propertylot')]
    operations = [
     migrations.AddField(model_name='set', name='is_active', field=models.BooleanField(default=True, verbose_name='is active')),
     migrations.AddField(model_name='set', name='is_link_to_lots', field=models.BooleanField(default=False, verbose_name='is link to lots')),
     migrations.AddField(model_name='set', name='set_of_lots', field=models.ManyToManyField(blank=True, to='condominium.PropertyLot', verbose_name='set of lots')),
     migrations.AddField(model_name='set', name='type_load', field=models.IntegerField(choices=[(0, 'current'), (1, 'exceptional')], db_index=True, default=0, verbose_name='type of load'))]