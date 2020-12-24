# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0018_auto_20170127_1513.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 623 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0017_merge_20170127_1350')]
    operations = [
     migrations.RemoveField(model_name='organization', name='hide_address'),
     migrations.AddField(model_name='organization', name='hidden_address', field=models.BooleanField(default=False, verbose_name='Hidden address'))]