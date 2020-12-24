# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matias/Documentos/MIS_MODULOS_PYTHON/matialvarezs_python_modules_creator/backend/apps/matialvarezs_charge_controller/migrations/0001_initial.py
# Compiled at: 2019-08-16 00:32:57
# Size of source mod 2**32: 1226 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='RegistersData', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'address', models.IntegerField(default=0)),
      (
       'code', models.CharField(default='', max_length=512)),
      (
       'count', models.IntegerField(default=1)),
      (
       'times', models.IntegerField(default=1)),
      (
       'unit', models.IntegerField(default=1)),
      (
       'function_code', models.IntegerField(default=0)),
      (
       'bits', models.BooleanField(default=False))], options={'abstract': False})]