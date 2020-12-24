# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0028_auto_20170126_1648.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 796 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_projects', '0027_auto_20170113_1746')]
    operations = [
     migrations.AlterField(model_name='apply', name='username', field=models.CharField(blank=True, max_length=200, null=True, verbose_name='name')),
     migrations.AlterField(model_name='project', name='image', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_uploads.UploadedImage', verbose_name='image'))]