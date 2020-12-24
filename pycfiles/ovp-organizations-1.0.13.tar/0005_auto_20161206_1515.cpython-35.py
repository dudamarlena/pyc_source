# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0005_auto_20161206_1515.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1020 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0003_uploadedimage_uuid'),
     ('ovp_organizations', '0004_organization_causes')]
    operations = [
     migrations.AddField(model_name='organization', name='image', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_uploads.UploadedImage')),
     migrations.AddField(model_name='organization', name='slug', field=models.SlugField(blank=True, max_length=100, null=True, unique=True)),
     migrations.AlterField(model_name='organization', name='facebook_page', field=models.CharField(blank=True, default=None, max_length=255, null=True))]