# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\migrations\0004_auto_20161218_1303.py
# Compiled at: 2017-01-15 02:22:00
# Size of source mod 2**32: 449 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nimble', '0003_auto_20161127_0953')]
    operations = [
     migrations.AlterField(model_name='story', name='title', field=models.CharField(max_length=100))]