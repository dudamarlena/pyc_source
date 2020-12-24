# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0087_auto_20190709_0836.py
# Compiled at: 2019-07-12 12:47:16
# Size of source mod 2**32: 1591 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0086_merge_20190507_1402')]
    operations = [
     migrations.CreateModel(name='WorkType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'inactive_flag', models.BooleanField(default=False))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False}),
     migrations.AddField(model_name='ticket',
       name='work_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='work_type_tickets', to='djconnectwise.WorkType')),
     migrations.AddField(model_name='timeentry',
       name='work_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.WorkType'))]