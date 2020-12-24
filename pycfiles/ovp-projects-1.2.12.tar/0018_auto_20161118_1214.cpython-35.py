# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0018_auto_20161118_1214.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 653 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0017_auto_20161118_1213')]
    operations = [
     migrations.RemoveField(model_name='work', name='can_be_done_remotely'),
     migrations.AlterField(model_name='work', name='description', field=models.CharField(default='-', max_length=4000, verbose_name='Description'), preserve_default=False)]