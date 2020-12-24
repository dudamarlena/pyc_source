# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/settings/migrations/0002_auto_20161231_1003.py
# Compiled at: 2016-12-31 04:03:06
# Size of source mod 2**32: 510 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('settings', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='settings', name='site_name', field=models.CharField(blank=True, default='PixelCMS site', max_length=255, verbose_name='site name'))]