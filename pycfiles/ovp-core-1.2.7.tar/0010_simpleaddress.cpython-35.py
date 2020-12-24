# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0010_simpleaddress.py
# Compiled at: 2017-06-13 14:17:51
# Size of source mod 2**32: 1117 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0009_lead_date')]
    operations = [
     migrations.CreateModel(name='SimpleAddress', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'street', models.CharField(blank=True, max_length=300, null=True)),
      (
       'number', models.CharField(blank=True, max_length=10, null=True)),
      (
       'neighbourhood', models.CharField(blank=True, max_length=100, null=True)),
      (
       'city', models.CharField(blank=True, max_length=100, null=True)),
      (
       'state', models.CharField(blank=True, max_length=100, null=True)),
      (
       'zipcode', models.CharField(blank=True, max_length=20, null=True)),
      (
       'country', models.CharField(blank=True, max_length=100, null=True))])]