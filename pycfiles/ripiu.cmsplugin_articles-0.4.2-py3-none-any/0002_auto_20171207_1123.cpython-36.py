# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0002_auto_20171207_1123.py
# Compiled at: 2018-02-20 05:54:14
# Size of source mod 2**32: 953 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filer', '0007_auto_20161016_1055'),
     ('cmsplugin_articles', '0001_initial')]
    operations = [
     migrations.AddField(model_name='articlepluginmodel',
       name='thumbnail_option',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filer.ThumbnailOption', verbose_name='thumbnail option')),
     migrations.AddField(model_name='sectionpluginmodel',
       name='thumbnail_option',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filer.ThumbnailOption', verbose_name='thumbnail option'))]