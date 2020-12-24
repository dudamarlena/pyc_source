# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0076_auto_20180925_1618.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1586 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0075_auto_20180910_1629')]
    operations = [
     migrations.CreateModel(name='Holiday',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=200)),
      (
       'all_day_flag', models.BooleanField(default=False)),
      (
       'date', models.DateField(blank=True, null=True)),
      (
       'start_time', models.TimeField(blank=True, null=True)),
      (
       'end_time', models.TimeField(blank=True, null=True))]),
     migrations.CreateModel(name='HolidayList',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=200))]),
     migrations.AddField(model_name='holiday',
       name='holiday_list',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.HolidayList')),
     migrations.AddField(model_name='calendar',
       name='holiday_list',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.HolidayList'))]