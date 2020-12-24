# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0001_initial.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 1329 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django_fido.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='U2fDevice',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'create_datetime', models.DateTimeField(auto_now_add=True)),
      (
       'version', models.TextField()),
      (
       'key_handle', models.TextField()),
      (
       'public_key', models.TextField()),
      (
       'app_id', models.TextField(blank=True, default=None, null=True)),
      (
       'raw_transports', models.TextField(blank=True, default=None, null=True, validators=[django_fido.models.TransportsValidator()])),
      (
       'counter', models.PositiveIntegerField(default=0)),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='u2f_devices', to=(settings.AUTH_USER_MODEL)))])]