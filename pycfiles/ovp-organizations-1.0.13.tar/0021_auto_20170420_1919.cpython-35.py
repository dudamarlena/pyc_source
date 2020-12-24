# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0021_auto_20170420_1919.py
# Compiled at: 2017-04-20 15:19:24
# Size of source mod 2**32: 531 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0020_auto_20170412_1609')]
    operations = [
     migrations.AlterField(model_name='organization', name='details', field=models.TextField(blank=True, default=None, max_length=3000, null=True, verbose_name='Details'))]