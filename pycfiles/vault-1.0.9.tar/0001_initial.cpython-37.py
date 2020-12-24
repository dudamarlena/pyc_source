# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/app/vault/vault/migrations/0001_initial.py
# Compiled at: 2020-03-17 15:36:46
# Size of source mod 2**32: 1762 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='CurrentProject',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'project', models.CharField(max_length=255)),
      (
       'user', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'db_table':'current_project', 
      'verbose_name_plural':'Current Project'}),
     migrations.CreateModel(name='GroupProjects',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'project', models.CharField(max_length=255)),
      (
       'owner', models.BooleanField(default=0)),
      (
       'group', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='auth.Group'))],
       options={'db_table':'group_projects', 
      'verbose_name_plural':'Groups and Projects'}),
     migrations.AlterUniqueTogether(name='groupprojects',
       unique_together=(set([('group', 'project')])))]