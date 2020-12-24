# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-licyilu1/django-cbr/cbr/migrations/0001_initial.py
# Compiled at: 2017-08-28 23:32:16
# Size of source mod 2**32: 1784 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='CBRCurrency', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=255, verbose_name='Name')),
      (
       'code', models.SlugField(unique=True)),
      (
       'num_code', models.SlugField()),
      (
       'char_code', models.SlugField())], options={'verbose_name_plural': 'Currencies', 
      'verbose_name': 'Currency', 
      'ordering': ['name']}),
     migrations.CreateModel(name='CBRCurrencyRate', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'date_rate', models.DateField(db_index=True, verbose_name='Date of rate')),
      (
       'nominal', models.PositiveSmallIntegerField(verbose_name='Nominal')),
      (
       'rate', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Rate')),
      (
       'currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbr.CBRCurrency', verbose_name='Currency'))], options={'verbose_name_plural': 'Rates of currency', 
      'verbose_name': 'Rate of currency', 
      'ordering': ['date_rate']})]