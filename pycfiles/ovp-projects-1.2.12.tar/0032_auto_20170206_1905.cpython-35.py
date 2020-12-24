# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0032_auto_20170206_1905.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 883 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0031_project_hidden_address')]
    operations = [
     migrations.AlterField(model_name='apply', name='status', field=models.CharField(choices=[('applied', 'Applied'), ('unapplied', 'Canceled')], default='applied', max_length=30, verbose_name='status')),
     migrations.AlterField(model_name='volunteerrole', name='project', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='ovp_projects.Project', verbose_name='Project'))]