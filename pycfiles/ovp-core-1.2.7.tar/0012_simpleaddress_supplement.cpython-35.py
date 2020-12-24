# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0012_simpleaddress_supplement.py
# Compiled at: 2017-06-20 14:52:04
# Size of source mod 2**32: 480 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0011_simpleaddress')]
    operations = [
     migrations.AddField(model_name='simpleaddress', name='supplement', field=models.CharField(blank=True, max_length=100, null=True))]