# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0003_auto_20161025_1609.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1404 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_core', '0004_load_skills_and_causes'),
     ('ovp_projects', '0002_auto_20161019_1557')]
    operations = [
     migrations.AddField(model_name='project', name='causes', field=models.ManyToManyField(to='ovp_core.Cause')),
     migrations.AddField(model_name='project', name='description', field=models.TextField(blank=True, max_length=160, null=True, verbose_name='Short description')),
     migrations.AddField(model_name='project', name='details', field=models.TextField(default='', max_length=3000, verbose_name='Details'), preserve_default=False),
     migrations.AddField(model_name='project', name='googleaddress', field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_core.GoogleAddress')),
     migrations.AddField(model_name='project', name='skills', field=models.ManyToManyField(to='ovp_core.Skill'))]