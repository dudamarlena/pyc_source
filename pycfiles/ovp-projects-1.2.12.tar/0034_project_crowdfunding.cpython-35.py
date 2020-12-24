# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0034_project_crowdfunding.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 493 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0033_auto_20170208_2118')]
    operations = [
     migrations.AddField(model_name='project', name='crowdfunding', field=models.BooleanField(default=False, verbose_name='Crowdfunding'))]