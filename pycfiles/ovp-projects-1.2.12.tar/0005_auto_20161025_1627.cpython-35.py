# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0005_auto_20161025_1627.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1329 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0004_auto_20161025_1626')]
    operations = [
     migrations.CreateModel(name='Availability', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'weekday', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (0, 'Sunday')], verbose_name='weekday')),
      (
       'period', models.PositiveSmallIntegerField(choices=[(0, 'Morning'), (1, 'Afternoon'), (2, 'Evening')], verbose_name='period'))], options={'verbose_name': 'availability'}),
     migrations.AlterField(model_name='job', name='dates', field=models.ManyToManyField(blank=True, to='ovp_projects.JobDate')),
     migrations.AddField(model_name='work', name='availabilities', field=models.ManyToManyField(to='ovp_projects.Availability'))]