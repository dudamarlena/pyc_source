# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0004_location.py
# Compiled at: 2016-02-11 15:47:00
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0003_user_is_private')]
    operations = [
     migrations.CreateModel(name=b'Location', fields=[
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'id', models.BigIntegerField(serialize=False, primary_key=True)),
      (
       b'name', models.CharField(max_length=100)),
      (
       b'latitude', models.FloatField()),
      (
       b'longitude', models.FloatField()),
      (
       b'street_address', models.CharField(max_length=100)),
      (
       b'media_count', models.PositiveIntegerField(null=True)),
      (
       b'media_feed', models.ManyToManyField(related_name=b'locations', to=b'instagram_api.Media'))], options={b'abstract': False}, bases=(
      models.Model,))]