# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0066_slapriority.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1377 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0065_auto_20180809_1124')]
    operations = [
     migrations.CreateModel(name='SlaPriority',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'respond_hours', models.BigIntegerField()),
      (
       'plan_within', models.BigIntegerField()),
      (
       'resolution_hours', models.BigIntegerField()),
      (
       'priority', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.TicketPriority')),
      (
       'sla', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.Sla'))],
       options={'ordering':('-modified', '-created'), 
      'get_latest_by':'modified', 
      'abstract':False})]