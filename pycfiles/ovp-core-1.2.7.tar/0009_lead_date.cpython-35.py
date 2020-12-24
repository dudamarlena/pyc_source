# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0009_lead_date.py
# Compiled at: 2017-06-13 14:16:15
# Size of source mod 2**32: 480 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0008_availability')]
    operations = [
     migrations.AddField(model_name='lead', name='date', field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date'))]