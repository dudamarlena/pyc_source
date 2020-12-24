# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/migrations/0009_cause_image.py
# Compiled at: 2017-06-13 14:16:40
# Size of source mod 2**32: 635 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0003_uploadedimage_uuid'),
     ('ovp_core', '0008_availability')]
    operations = [
     migrations.AddField(model_name='cause', name='image', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_uploads.UploadedImage', verbose_name='image'))]