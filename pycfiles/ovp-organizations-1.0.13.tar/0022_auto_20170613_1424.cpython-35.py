# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0022_auto_20170613_1424.py
# Compiled at: 2017-06-13 10:25:37
# Size of source mod 2**32: 476 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0021_auto_20170420_1919')]
    operations = [
     migrations.AlterModelOptions(name='organization', options={'verbose_name': 'organization', 'verbose_name_plural': 'organizations'})]