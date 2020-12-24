# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0030_passwordhistory_set_date.py
# Compiled at: 2017-05-22 20:56:54
# Size of source mod 2**32: 478 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0029_passwordhistory')]
    operations = [
     migrations.AddField(model_name='passwordhistory', name='set_date', field=models.DateTimeField(auto_now_add=True, null=True))]