# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/migrations/0006_auto_20170613_1424.py
# Compiled at: 2017-06-13 10:27:08
# Size of source mod 2**32: 472 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0005_auto_20170522_2006')]
    operations = [
     migrations.AlterModelOptions(name='imagegalery', options={'verbose_name': 'image gallery', 'verbose_name_plural': 'image galleries'})]