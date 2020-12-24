# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0022_auto_20161220_1914.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 892 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0021_project_max_applies_from_roles')]
    operations = [
     migrations.RemoveField(model_name='job', name='dates'),
     migrations.AddField(model_name='jobdate', name='job', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='ovp_projects.Job')),
     migrations.AlterField(model_name='jobdate', name='name', field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Label'))]