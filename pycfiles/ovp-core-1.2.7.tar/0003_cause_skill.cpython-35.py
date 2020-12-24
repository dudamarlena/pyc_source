# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0003_cause_skill.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1106 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0002_auto_20161019_1557')]
    operations = [
     migrations.CreateModel(name='Cause', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='name'))], options={'verbose_name': 'cause', 
      'verbose_name_plural': 'causes'}),
     migrations.CreateModel(name='Skill', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='name'))], options={'verbose_name': 'skill'})]