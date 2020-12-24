# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0002_auto_20160907_2116.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 1178 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0001_initial')]
    operations = [
     migrations.AddField(model_name='user', name='is_active', field=models.BooleanField(default=True, verbose_name='Active')),
     migrations.AddField(model_name='user', name='is_email_verified', field=models.BooleanField(default=False, verbose_name='Email verified')),
     migrations.AddField(model_name='user', name='is_staff', field=models.BooleanField(default=False, verbose_name='Staff')),
     migrations.AddField(model_name='user', name='joined_date', field=models.DateTimeField(auto_now_add=True, null=True)),
     migrations.AddField(model_name='user', name='modified_date', field=models.DateTimeField(auto_now=True, null=True))]