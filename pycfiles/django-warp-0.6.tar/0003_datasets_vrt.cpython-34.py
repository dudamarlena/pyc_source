# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/urb/Dropbox/dev/django-warp/django_warp/migrations/0003_datasets_vrt.py
# Compiled at: 2017-09-04 03:15:48
# Size of source mod 2**32: 471 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_warp', '0002_auto_20170727_0821')]
    operations = [
     migrations.AddField(model_name='datasets', name='vrt', field=models.FileField(blank=True, null=True, upload_to=''))]