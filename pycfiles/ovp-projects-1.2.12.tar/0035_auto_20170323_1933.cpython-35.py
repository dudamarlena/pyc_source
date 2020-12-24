# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0035_auto_20170323_1933.py
# Compiled at: 2017-04-03 15:52:58
# Size of source mod 2**32: 646 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0034_project_crowdfunding')]
    operations = [
     migrations.AlterField(model_name='apply', name='status', field=models.CharField(choices=[('applied', 'Applied'), ('unapplied', 'Canceled'), ('confirmed-volunteer', 'Confirmed Volunteer'), ('not-volunteer', 'Not a Volunteer')], default='applied', max_length=30, verbose_name='status'))]