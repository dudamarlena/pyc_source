# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0005_auto_20170111_1633.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 417 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0004_load_skills_and_causes')]
    operations = [
     migrations.AlterModelOptions(name='cause', options={'verbose_name': 'cause'})]