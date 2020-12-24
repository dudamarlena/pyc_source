# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0011_auto_20161115_1744.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1220 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0010_auto_20161102_2131')]
    operations = [
     migrations.AlterModelOptions(name='availability', options={'verbose_name': 'availability', 'verbose_name_plural': 'availabilities'}),
     migrations.AlterModelOptions(name='job', options={'verbose_name': 'job', 'verbose_name_plural': 'jobs'}),
     migrations.AlterModelOptions(name='jobdate', options={'verbose_name': 'job date', 'verbose_name_plural': 'job dates'}),
     migrations.AlterModelOptions(name='project', options={'verbose_name': 'project', 'verbose_name_plural': 'projects'}),
     migrations.AlterModelOptions(name='role', options={'verbose_name': 'volunteer role', 'verbose_name_plural': 'volunteer roles'}),
     migrations.RemoveField(model_name='project', name='roles')]