# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0024_auto_20170112_1644.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 698 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0023_auto_20170112_1417')]
    operations = [
     migrations.AddField(model_name='apply', name='phone', field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone')),
     migrations.AddField(model_name='apply', name='username', field=models.CharField(blank=True, max_length=200, null=True, verbose_name='username'))]