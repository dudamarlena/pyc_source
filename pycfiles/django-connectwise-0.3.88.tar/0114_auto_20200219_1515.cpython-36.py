# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0114_auto_20200219_1515.py
# Compiled at: 2020-02-20 12:46:44
# Size of source mod 2**32: 1351 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0113_auto_20200204_1054')]
    operations = [
     migrations.CreateModel(name='ProjectType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=30)),
      (
       'default_flag', models.BooleanField(default=False)),
      (
       'inactive_flag', models.BooleanField(default=False))],
       options={'verbose_name_plural':'Project types', 
      'ordering':('name', )}),
     migrations.AddField(model_name='project',
       name='type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.ProjectType'))]