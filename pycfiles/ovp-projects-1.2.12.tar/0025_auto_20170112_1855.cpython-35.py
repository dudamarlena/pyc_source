# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0025_auto_20170112_1855.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 945 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0024_auto_20170112_1644')]
    operations = [
     migrations.AddField(model_name='project', name='max_applies', field=models.IntegerField(default=1)),
     migrations.AddField(model_name='project', name='public_project', field=models.BooleanField(default=True, verbose_name='Public')),
     migrations.AlterField(model_name='project', name='owner', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'))]