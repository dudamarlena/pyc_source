# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aneumeier/github/userprofile/userprofile/migrations/0001_initial.py
# Compiled at: 2015-11-27 14:34:28
# Size of source mod 2**32: 1077 bytes
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Profile', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'is_public', models.BooleanField(default=False)),
      (
       'gender', models.CharField(default=b'u', max_length=1, choices=[(b'u', 'undefined'), (b'M', 'Male'), (b'F', 'Female')])),
      (
       'lookfor', models.CharField(default=b'a', max_length=1, choices=[(b'a', 'any'), (b'M', 'Man'), (b'F', 'Female')])),
      (
       'dob', models.DateField(null=True, blank=True)),
      (
       'user', models.OneToOneField(to=settings.AUTH_USER_MODEL))], options={}, bases=(
      models.Model,))]