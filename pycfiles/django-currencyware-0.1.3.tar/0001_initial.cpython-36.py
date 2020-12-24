# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-tisqp5jr/django-currencyware/currencyware/migrations/0001_initial.py
# Compiled at: 2018-08-22 09:57:42
# Size of source mod 2**32: 2068 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Currency',
       fields=[
      (
       'code', models.CharField(help_text='Currency code', max_length=3, primary_key=True, serialize=False, verbose_name='Code')),
      (
       'name', models.CharField(blank=True, help_text='Curreny name (english)', max_length=60, null=True, verbose_name='Name')),
      (
       'number', models.CharField(blank=True, help_text='Numeric code', max_length=3, null=True, verbose_name='Number')),
      (
       'unit', models.IntegerField(blank=True, help_text='Currency unit', null=True, verbose_name='Unit')),
      (
       'symbol', models.CharField(blank=True, help_text='Currency symbol', max_length=10, null=True, verbose_name='Symbol')),
      (
       'country', models.CharField(blank=True, help_text='Primary currency in these countries', max_length=255, null=True, verbose_name='Country'))],
       options={'verbose_name':'Currency', 
      'verbose_name_plural':'Currencies'}),
     migrations.CreateModel(name='Rate',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'code', models.CharField(help_text='Currency code', max_length=3, verbose_name='Code')),
      (
       'name', models.CharField(blank=True, help_text='Curreny name (english)', max_length=100, null=True, verbose_name='Name')),
      (
       'rate', models.FloatField(default=0.0, help_text='Currency forex rate', verbose_name='Rate')),
      (
       'date', models.DateTimeField(help_text="Rate's date", verbose_name='Date'))],
       options={'verbose_name':'Rate', 
      'verbose_name_plural':'Rates'})]