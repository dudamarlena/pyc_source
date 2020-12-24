# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starline/git/django-gerencianet/gerencianet/migrations/0001_initial.py
# Compiled at: 2015-10-19 13:26:05
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'PaymentLog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'timestamp', models.DateTimeField(auto_now=True)),
      (
       b'data', models.TextField()),
      (
       b'email', models.EmailField(max_length=254, null=True))])]