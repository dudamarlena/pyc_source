# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0015_auto_20161116_0141.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 582 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0014_apply')]
    operations = [
     migrations.AddField(model_name='project', name='applied_count', field=models.IntegerField(default=0)),
     migrations.AlterUniqueTogether(name='apply', unique_together=set([('email', 'project')]))]