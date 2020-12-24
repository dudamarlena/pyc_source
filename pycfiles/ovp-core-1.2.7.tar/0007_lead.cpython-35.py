# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0007_lead.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1044 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0006_merge_20170112_2144')]
    operations = [
     migrations.CreateModel(name='Lead', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
      (
       'email', models.CharField(max_length=100, verbose_name='Email')),
      (
       'phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Phone')),
      (
       'country', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country'))], options={'verbose_name_plural': 'Leads', 
      'verbose_name': 'Lead'})]