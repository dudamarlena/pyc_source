# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0035_activity.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1507 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0034_auto_20170727_1243')]
    operations = [
     migrations.CreateModel(name='Activity',
       fields=[
      (
       'id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=250)),
      (
       'notes', models.TextField(blank=True, null=True, max_length=2000)),
      (
       'date_start', models.DateTimeField(blank=True, null=True)),
      (
       'date_end', models.DateTimeField(blank=True, null=True)),
      (
       'assign_to', models.ForeignKey(to='djconnectwise.Member', on_delete=(models.CASCADE))),
      (
       'opportunity', models.ForeignKey(null=True, blank=True, to='djconnectwise.Opportunity', on_delete=(models.CASCADE))),
      (
       'ticket', models.ForeignKey(null=True, blank=True, to='djconnectwise.Ticket', on_delete=(models.CASCADE)))],
       options={'verbose_name_plural': 'activities'})]