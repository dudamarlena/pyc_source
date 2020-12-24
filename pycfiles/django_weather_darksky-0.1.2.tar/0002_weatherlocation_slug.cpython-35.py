# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/slava/myprojects/cbr/django_weather_darksky/migrations/0002_weatherlocation_slug.py
# Compiled at: 2017-03-21 00:08:22
# Size of source mod 2**32: 513 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_weather_darksky', '0001_initial')]
    operations = [
     migrations.AddField(model_name='weatherlocation', name='slug', field=models.SlugField(default=1, verbose_name='Slug'), preserve_default=False)]