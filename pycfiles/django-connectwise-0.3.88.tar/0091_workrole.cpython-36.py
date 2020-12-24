# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0091_workrole.py
# Compiled at: 2019-07-18 14:57:10
# Size of source mod 2**32: 1045 bytes
from django.db import migrations, models
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0090_auto_20190711_1114')]
    operations = [
     migrations.CreateModel(name='WorkRole',
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
      'abstract':False})]