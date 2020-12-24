# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0016_organization_hide_address.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 504 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0015_merge_20170112_2144')]
    operations = [
     migrations.AddField(model_name='organization', name='hide_address', field=models.BooleanField(default=False, verbose_name='Hide address'))]