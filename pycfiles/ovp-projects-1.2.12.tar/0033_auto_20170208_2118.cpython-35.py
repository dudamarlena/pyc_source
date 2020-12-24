# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0033_auto_20170208_2118.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 500 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0032_auto_20170206_1905')]
    operations = [
     migrations.AlterField(model_name='apply', name='email', field=models.CharField(blank=True, max_length=190, null=True, verbose_name='email'))]