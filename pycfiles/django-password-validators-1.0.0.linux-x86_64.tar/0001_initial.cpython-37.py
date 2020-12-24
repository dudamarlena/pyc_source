# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/password_history/migrations/0001_initial.py
# Compiled at: 2020-01-08 09:44:25
# Size of source mod 2**32: 2543 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='PasswordHistory',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'password', models.CharField(editable=False, max_length=255, verbose_name='Password hash')),
      (
       'date', models.DateTimeField(auto_now_add=True, verbose_name='Date'))],
       options={'ordering':[
       '-user_config', 'password'], 
      'verbose_name':'Old password', 
      'verbose_name_plural':'Password history'}),
     migrations.CreateModel(name='UserPasswordHistoryConfig',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'date', models.DateTimeField(auto_now_add=True, verbose_name='When created salt')),
      (
       'salt', models.CharField(editable=False, max_length=120, verbose_name='Salt for the user')),
      (
       'iterations', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='The number of of iterations for Hasher')),
      (
       'user', models.ForeignKey(editable=False, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'ordering':[
       '-user', 'iterations'], 
      'verbose_name':'Configuration', 
      'verbose_name_plural':'Configurations'}),
     migrations.AddField(model_name='passwordhistory',
       name='user_config',
       field=models.ForeignKey(editable=False, on_delete=(django.db.models.deletion.CASCADE), to='password_history.UserPasswordHistoryConfig')),
     migrations.AlterUniqueTogether(name='userpasswordhistoryconfig',
       unique_together=(set([('user', 'iterations')]))),
     migrations.AlterUniqueTogether(name='passwordhistory',
       unique_together=(set([('user_config', 'password')])))]