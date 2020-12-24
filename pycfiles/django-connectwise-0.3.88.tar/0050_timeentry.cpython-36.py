# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0050_timeentry.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1947 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0049_auto_20180205_1122')]
    operations = [
     migrations.CreateModel(name='TimeEntry',
       fields=[
      (
       'id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
      (
       'charge_to_type', models.CharField(choices=[('ServiceTicket', 'Service Ticket'), ('ProjectTicket', 'Project Ticket'), ('ChargeCode', 'Charge Code'), ('Activity', 'Activity')], max_length=250, db_index=True)),
      (
       'billable_option', models.CharField(choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge'), ('NoDefault', 'No Default')], max_length=250, db_index=True)),
      (
       'time_start', models.DateTimeField(null=True, blank=True)),
      (
       'time_end', models.DateTimeField(null=True, blank=True)),
      (
       'hours_deduct', models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=6)),
      (
       'actual_hours', models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=6)),
      (
       'notes', models.TextField(max_length=2000, null=True, blank=True)),
      (
       'internal_notes', models.TextField(max_length=2000, null=True, blank=True)),
      (
       'charge_to_id', models.ForeignKey(null=True, blank=True, to='djconnectwise.Ticket', on_delete=(models.CASCADE))),
      (
       'company', models.ForeignKey(to='djconnectwise.Company', on_delete=(models.CASCADE))),
      (
       'member', models.ForeignKey(null=True, blank=True, to='djconnectwise.Member', on_delete=(models.CASCADE)))],
       options={'verbose_name_plural':'Time Entries', 
      'ordering':('id', )})]