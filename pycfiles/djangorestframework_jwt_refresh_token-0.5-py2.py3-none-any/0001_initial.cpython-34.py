# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/src/django-rest-framework-jwt-refresh-token/refreshtoken/migrations/0001_initial.py
# Compiled at: 2016-01-28 09:27:04
# Size of source mod 2**32: 1022 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='RefreshToken', fields=[
      (
       'key', models.CharField(max_length=40, primary_key=True, serialize=False)),
      (
       'app', models.CharField(max_length=255)),
      (
       'created', models.DateTimeField(auto_now_add=True)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refresh_tokens', to=settings.AUTH_USER_MODEL))]),
     migrations.AlterUniqueTogether(name='refreshtoken', unique_together=set([('user', 'app')]))]