# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0004_auto_20171213_1327.py
# Compiled at: 2018-02-20 05:54:14
# Size of source mod 2**32: 885 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles', '0003_auto_20171207_1310')]
    operations = [
     migrations.AddField(model_name='articlepluginmodel',
       name='header_alignment',
       field=models.CharField(blank=True, choices=[('left', 'left'), ('right', 'right'), ('center', 'center')], max_length=10, verbose_name='header alignment')),
     migrations.AddField(model_name='sectionpluginmodel',
       name='header_alignment',
       field=models.CharField(blank=True, choices=[('left', 'left'), ('right', 'right'), ('center', 'center')], max_length=10, verbose_name='header alignment'))]