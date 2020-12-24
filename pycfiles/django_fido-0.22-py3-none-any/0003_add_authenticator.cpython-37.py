# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/migrations/0003_add_authenticator.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 1021 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('django_fido', '0002_u2fdevice_attestation')]
    operations = [
     migrations.CreateModel(name='Authenticator',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'create_datetime', models.DateTimeField(auto_now_add=True)),
      (
       'credential_data', models.TextField()),
      (
       'counter', models.PositiveIntegerField(default=0)),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='authenticators', to=(settings.AUTH_USER_MODEL)))])]