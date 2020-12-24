# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0010_auto_20161102_2131.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 575 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0009_auto_20161102_2122')]
    operations = [
     migrations.AlterField(model_name='project', name='organization', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_organizations.Organization'))]