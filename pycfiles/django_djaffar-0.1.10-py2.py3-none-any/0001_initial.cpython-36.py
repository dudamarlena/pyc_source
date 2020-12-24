# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/arnaudrenaud/django-djaffar/djaffar/migrations/0001_initial.py
# Compiled at: 2016-12-27 03:30:12
# Size of source mod 2**32: 1516 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('sessions', '0001_initial')]
    operations = [
     migrations.CreateModel(name='SessionInfo',
       fields=[
      (
       'session', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), primary_key=True, serialize=False, to='sessions.Session')),
      (
       'user_agent', models.CharField(max_length=1000))]),
     migrations.CreateModel(name='Activity',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'ip_address', models.CharField(default='', max_length=45)),
      (
       'date', models.DateTimeField()),
      (
       'path', models.CharField(max_length=1000)),
      (
       'referer', models.CharField(default='', max_length=160)),
      (
       'session', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), to='sessions.Session')),
      (
       'user', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))])]