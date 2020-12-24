# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0020_work_can_be_done_remotely.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 515 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0019_auto_20161121_0140')]
    operations = [
     migrations.AddField(model_name='work', name='can_be_done_remotely', field=models.BooleanField(default=False, verbose_name='This job can be done remotely'))]