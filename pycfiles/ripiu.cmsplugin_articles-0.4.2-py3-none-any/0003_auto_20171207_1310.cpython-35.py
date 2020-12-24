# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0003_auto_20171207_1310.py
# Compiled at: 2018-02-20 05:54:14
# Size of source mod 2**32: 891 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles', '0002_auto_20171207_1123')]
    operations = [
     migrations.AddField(model_name='articlepluginmodel', name='alignment', field=models.CharField(blank=True, choices=[('left', 'left'), ('right', 'right'), ('center', 'center')], max_length=10, null=True, verbose_name='image alignment')),
     migrations.AddField(model_name='sectionpluginmodel', name='alignment', field=models.CharField(blank=True, choices=[('left', 'left'), ('right', 'right'), ('center', 'center')], max_length=10, null=True, verbose_name='image alignment'))]