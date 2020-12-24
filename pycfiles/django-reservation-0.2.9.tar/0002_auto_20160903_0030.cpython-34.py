# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/organilab/djreservation/migrations/0002_auto_20160903_0030.py
# Compiled at: 2016-09-03 02:30:30
# Size of source mod 2**32: 1092 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djreservation', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Observation', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'text', models.TextField())]),
     migrations.AlterField(model_name='reservation', name='status', field=models.SmallIntegerField(choices=[(0, 'building'), (1, 'Requested'), (2, 'Acepted'), (3, 'Denied'), (4, 'Borrowed'), (5, 'Returned')], default=0)),
     migrations.AddField(model_name='observation', name='reservation', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreservation.Reservation'))]