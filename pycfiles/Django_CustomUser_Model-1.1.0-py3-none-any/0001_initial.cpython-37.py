# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghorz/Desktop/works/django3/user_proj/user_app/migrations/0001_initial.py
# Compiled at: 2020-03-19 09:14:28
# Size of source mod 2**32: 2068 bytes
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('auth', '0011_update_proxy_permissions')]
    operations = [
     migrations.CreateModel(name='CustomUserProfile',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'password', models.CharField(max_length=128, verbose_name='password')),
      (
       'last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
      (
       'is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
      (
       'email', models.EmailField(max_length=255, unique=True)),
      (
       'first_name', models.CharField(max_length=50)),
      (
       'last_name', models.CharField(max_length=50)),
      (
       'middle_name', models.CharField(blank=True, max_length=50, null=True)),
      (
       'photo', models.ImageField(upload_to='photo')),
      (
       'is_active', models.BooleanField(default=True)),
      (
       'is_staff', models.BooleanField(default=False)),
      (
       'date_joined', models.DateTimeField(default=(datetime.datetime(2020, 3, 19, 13, 14, 27, 119955)))),
      (
       'groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
      (
       'user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'))],
       options={'abstract': False})]