# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0051_opportunitynote.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1089 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0050_servicenote')]
    operations = [
     migrations.CreateModel(name='OpportunityNote',
       fields=[
      (
       'id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', auto_now=True)),
      (
       'text', models.TextField(blank=True, null=True, max_length=2000)),
      (
       'opportunity', models.ForeignKey(to='djconnectwise.Opportunity', on_delete=(models.CASCADE)))],
       options={'verbose_name_plural':'Opportunity Notes', 
      'ordering':('id', )})]