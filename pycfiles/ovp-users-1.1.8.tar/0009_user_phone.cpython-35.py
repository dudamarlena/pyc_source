# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0009_user_phone.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 493 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0008_auto_20161007_2052')]
    operations = [
     migrations.AddField(model_name='user', name='phone', field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Phone'))]