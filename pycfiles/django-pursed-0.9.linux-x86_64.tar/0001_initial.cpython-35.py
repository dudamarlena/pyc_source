# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/migrations/0001_initial.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 1571 bytes
from __future__ import unicode_literals
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Transaction', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'value', models.BigIntegerField(default=0)),
      (
       'running_balance', models.BigIntegerField(default=0)),
      (
       'created_at', models.DateTimeField(default=datetime.datetime.utcnow))]),
     migrations.CreateModel(name='Wallet', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'current_balance', models.BigIntegerField(default=0)),
      (
       'created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.AddField(model_name='transaction', name='wallet', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.Wallet'))]