# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/test_mocks/migrations/0001_initial.py
# Compiled at: 2016-03-10 19:05:53
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone, slothauth.managers, slothauth.utils

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('auth', '0007_alter_validators_add_error_messages')]
    operations = [
     migrations.CreateModel(name=b'Account', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'password', models.CharField(max_length=128, verbose_name=b'password')),
      (
       b'last_login', models.DateTimeField(blank=True, null=True, verbose_name=b'last login')),
      (
       b'is_superuser', models.BooleanField(default=False, help_text=b'Designates that this user has all permissions without explicitly assigning them.', verbose_name=b'superuser status')),
      (
       b'first_name', models.CharField(blank=True, max_length=30, verbose_name=b'first name')),
      (
       b'last_name', models.CharField(blank=True, max_length=30, verbose_name=b'last name')),
      (
       b'email', models.EmailField(max_length=254, unique=True, verbose_name=b'email address')),
      (
       b'is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
      (
       b'is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
      (
       b'date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
      (
       b'passwordless_key', slothauth.utils.RandomField(max_length=32)),
      (
       b'one_time_authentication_key', slothauth.utils.RandomField(max_length=32)),
      (
       b'password_reset_key', slothauth.utils.RandomField(max_length=32)),
      (
       b'groups', models.ManyToManyField(blank=True, help_text=b'The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name=b'user_set', related_query_name=b'user', to=b'auth.Group', verbose_name=b'groups')),
      (
       b'user_permissions', models.ManyToManyField(blank=True, help_text=b'Specific permissions for this user.', related_name=b'user_set', related_query_name=b'user', to=b'auth.Permission', verbose_name=b'user permissions'))], options={b'abstract': False}, managers=[
      (
       b'objects', slothauth.managers.UserManager())])]