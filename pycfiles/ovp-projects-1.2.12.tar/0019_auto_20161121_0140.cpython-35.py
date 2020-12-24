# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0019_auto_20161121_0140.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 801 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0018_auto_20161118_1214')]
    operations = [
     migrations.AlterField(model_name='jobdate', name='end_date', field=models.DateTimeField(default=timezone.now(), verbose_name='End date'), preserve_default=False),
     migrations.AlterField(model_name='jobdate', name='start_date', field=models.DateTimeField(default=timezone.now(), verbose_name='Start date'), preserve_default=False)]