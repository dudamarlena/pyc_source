# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0001_initial.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 1036 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='User', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'password', models.CharField(max_length=128, verbose_name='password')),
      (
       'last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
      (
       'email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
      (
       'name', models.CharField(max_length=200, verbose_name='Name')),
      (
       'slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Slug'))], options={'abstract': False})]