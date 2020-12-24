# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0003_auto_20160907_2123.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 505 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0002_auto_20160907_2116')]
    operations = [
     migrations.AlterField(model_name='user', name='slug', field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug'))]