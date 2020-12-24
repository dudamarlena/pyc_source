# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0108_projectphase.py
# Compiled at: 2019-08-21 18:56:27
# Size of source mod 2**32: 2112 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0107_auto_20190729_1352')]
    operations = [
     migrations.CreateModel(name='ProjectPhase',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'description', models.CharField(max_length=100)),
      (
       'scheduled_start', models.DateField(blank=True, null=True)),
      (
       'scheduled_end', models.DateField(blank=True, null=True)),
      (
       'actual_start', models.DateField(blank=True, null=True)),
      (
       'actual_end', models.DateField(blank=True, null=True)),
      (
       'bill_time', models.CharField(blank=True, choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge')], max_length=50, null=True)),
      (
       'notes', models.TextField(null=True)),
      (
       'scheduled_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'actual_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'budget_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
      (
       'board', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.ConnectWiseBoard')),
      (
       'project', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Project'))],
       options={'verbose_name_plural': 'Project phases'})]