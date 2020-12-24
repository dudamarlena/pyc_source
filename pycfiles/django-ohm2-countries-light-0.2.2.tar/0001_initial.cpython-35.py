# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev-light/application/backend/apps/ohm2_countries_light/migrations/0001_initial.py
# Compiled at: 2017-08-01 00:07:17
# Size of source mod 2**32: 1576 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
import django.utils.timezone, ohm2_countries_light.managers

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Country', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'name', models.CharField(max_length=512, validators=[django.core.validators.MinLengthValidator(1)])),
      (
       'official_name', models.CharField(max_length=512, validators=[django.core.validators.MinLengthValidator(1)])),
      (
       'alpha_2', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(2)])),
      (
       'alpha_3', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(3)])),
      (
       'numeric', models.IntegerField()),
      (
       'flag_small', models.ImageField(upload_to=ohm2_countries_light.managers.country_flag_small_upload_to))], options={'abstract': False})]