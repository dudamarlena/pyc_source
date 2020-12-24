# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/migrations/0003_uploadedimage_uuid.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 500 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0002_uploadedimage')]
    operations = [
     migrations.AddField(model_name='uploadedimage', name='uuid', field=models.CharField(blank=True, default=None, max_length=36, verbose_name='UUID'))]