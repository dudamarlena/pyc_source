# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0007_project_image.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 652 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0003_uploadedimage_uuid'),
     ('ovp_projects', '0006_auto_20161025_1726')]
    operations = [
     migrations.AddField(model_name='project', name='image', field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ovp_uploads.UploadedImage'), preserve_default=False)]