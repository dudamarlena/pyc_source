# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0065_auto_20180809_1124.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 2239 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0064_auto_20180808_1214')]
    operations = [
     migrations.CreateModel(name='Calendar',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=250)),
      (
       'monday_start_time', models.TimeField(blank=True, null=True)),
      (
       'monday_end_time', models.TimeField(blank=True, null=True)),
      (
       'tuesday_start_time', models.TimeField(blank=True, null=True)),
      (
       'tuesday_end_time', models.TimeField(blank=True, null=True)),
      (
       'wednesday_start_time', models.TimeField(blank=True, null=True)),
      (
       'wednesday_end_time', models.TimeField(blank=True, null=True)),
      (
       'thursday_start_time', models.TimeField(blank=True, null=True)),
      (
       'thursday_end_time', models.TimeField(blank=True, null=True)),
      (
       'friday_start_time', models.TimeField(blank=True, null=True)),
      (
       'friday_end_time', models.TimeField(blank=True, null=True)),
      (
       'saturday_start_time', models.TimeField(blank=True, null=True)),
      (
       'saturday_end_time', models.TimeField(blank=True, null=True)),
      (
       'sunday_start_time', models.TimeField(blank=True, null=True)),
      (
       'sunday_end_time', models.TimeField(blank=True, null=True))]),
     migrations.AddField(model_name='sla',
       name='based_on',
       field=models.CharField(choices=[('MyCalendar', 'My Company Calendar'), ('Customer', "Customer's Calendar"), ('AllHours', '24 Hours'), ('Custom', 'Custom Calendar')], db_index=True, default='MyCalendar', max_length=50)),
     migrations.AddField(model_name='sla',
       name='calendar',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Calendar'))]