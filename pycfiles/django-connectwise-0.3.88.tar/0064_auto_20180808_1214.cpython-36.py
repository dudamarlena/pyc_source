# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0064_auto_20180808_1214.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1509 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0063_merge_20180611_0905')]
    operations = [
     migrations.CreateModel(name='Sla',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.TextField(max_length=250)),
      (
       'default_flag', models.BooleanField(default=False)),
      (
       'respond_hours', models.BigIntegerField()),
      (
       'plan_within', models.BigIntegerField()),
      (
       'resolution_hours', models.BigIntegerField())],
       options={'ordering':('-modified', '-created'), 
      'abstract':False, 
      'get_latest_by':'modified'}),
     migrations.AddField(model_name='ticket',
       name='sla',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='tickets', to='djconnectwise.Sla'))]