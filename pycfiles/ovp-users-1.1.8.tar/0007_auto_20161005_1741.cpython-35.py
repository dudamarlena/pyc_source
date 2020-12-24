# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0007_auto_20161005_1741.py
# Compiled at: 2016-11-29 13:10:11
# Size of source mod 2**32: 446 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0006_auto_20161005_1651')]
    operations = [
     migrations.RenameField(model_name='passwordrecoverytoken', old_name='used', new_name='used_date')]