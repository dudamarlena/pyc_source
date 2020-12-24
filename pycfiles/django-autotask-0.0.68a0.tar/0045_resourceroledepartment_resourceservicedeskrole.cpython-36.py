# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0045_resourceroledepartment_resourceservicedeskrole.py
# Compiled at: 2020-02-06 17:58:37
# Size of source mod 2**32: 1647 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0044_merge_20200205_1651')]
    operations = [
     migrations.CreateModel(name='ResourceRoleDepartment',
       fields=[
      (
       'id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
      (
       'active', models.BooleanField(default=True)),
      (
       'default', models.BooleanField(default=False)),
      (
       'department_lead', models.BooleanField(default=False)),
      (
       'department', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Department')),
      (
       'resource', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Resource')),
      (
       'role', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Role'))]),
     migrations.CreateModel(name='ResourceServiceDeskRole',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'active', models.BooleanField(default=True)),
      (
       'default', models.BooleanField(default=False)),
      (
       'resource', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Resource')),
      (
       'role', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djautotask.Role'))])]