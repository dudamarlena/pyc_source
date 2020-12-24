# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0002_service_is_available.py
# Compiled at: 2016-03-22 05:48:15
# Size of source mod 2**32: 478 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0001_initial')]
    operations = [
     migrations.AddField(model_name='service',
       name='is_available',
       field=models.BooleanField(default=True, verbose_name='Is available ?'))]