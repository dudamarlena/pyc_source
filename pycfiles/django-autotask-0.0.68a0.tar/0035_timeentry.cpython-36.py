# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0035_timeentry.py
# Compiled at: 2020-01-27 17:48:13
# Size of source mod 2**32: 2114 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0034_auto_20191210_1518')]
    operations = [
     migrations.CreateModel(name='TimeEntry',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'date_worked', models.DateTimeField(blank=True, null=True)),
      (
       'start_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'end_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'summary_notes', models.TextField(blank=True, max_length=8000, null=True)),
      (
       'internal_notes', models.TextField(blank=True, max_length=8000, null=True)),
      (
       'non_billable', models.BooleanField(default=False)),
      (
       'hours_worked', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'hours_to_bill', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'offset_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'resource', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Resource')),
      (
       'task', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Task')),
      (
       'ticket', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Ticket'))],
       options={'verbose_name_plural': 'Time entries'})]