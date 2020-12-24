# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0013_auto_20170208_2118.py
# Compiled at: 2017-05-15 11:01:22
# Size of source mod 2**32: 488 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_users', '0012_merge_20170112_2144')]
    operations = [
     migrations.AlterField(model_name='user', name='email', field=models.EmailField(max_length=190, unique=True, verbose_name='Email'))]