# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/Dropbox/dev/django-warp/django_warp/migrations/0004_datasets_transparency.py
# Compiled at: 2017-09-07 07:42:12
# Size of source mod 2**32: 491 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_warp', '0003_datasets_vrt')]
    operations = [
     migrations.AddField(model_name='datasets', name='transparency', field=models.BooleanField(default=False), preserve_default=False)]