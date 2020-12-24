# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0024_opportunitystage.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1000 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0023_auto_20170605_0705')]
    operations = [
     migrations.CreateModel(name='OpportunityStage',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True)),
      (
       'name', models.CharField(max_length=50))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False})]