# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0013_project_roles.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 522 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0012_auto_20161115_1745')]
    operations = [
     migrations.AddField(model_name='project', name='roles', field=models.ManyToManyField(blank=True, to='ovp_projects.VolunteerRole', verbose_name='Volunteer Roles'))]