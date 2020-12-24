# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0096_agreement.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 1469 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0095_connectwiseboard_work_type')]
    operations = [
     migrations.CreateModel(name='Agreement',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=100)),
      (
       'bill_time', models.CharField(blank=True, choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge')], max_length=50, null=True)),
      (
       'work_role', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.WorkRole')),
      (
       'work_type', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.WorkType'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False})]