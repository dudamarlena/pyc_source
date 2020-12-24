# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/migrations/0002_alias.py
# Compiled at: 2017-01-05 12:36:46
# Size of source mod 2**32: 1191 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('accounts', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Alias', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'name', models.CharField(max_length=512, unique=True)),
      (
       'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'abstract': False})]