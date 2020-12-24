# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0025_remove_userprofile_public.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 393 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0024_user_public')]
    operations = [
     migrations.RemoveField(model_name='userprofile', name='public')]