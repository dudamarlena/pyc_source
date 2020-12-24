# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yohann/Dev/django-pg-badges/demo/venv/lib/python2.7/site-packages/badges/migrations/0001_initial.py
# Compiled at: 2016-01-24 17:15:15
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Badge', fields=[
      (
       b'id',
       models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.TextField()),
      (
       b'code', models.CharField(max_length=100)),
      (
       b'user',
       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.AlterUniqueTogether(name=b'badge', unique_together=set([('user', 'name')]))]