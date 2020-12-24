# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_rototalc/ripiu/cmsplugin_rototalc/migrations/0003_auto_20171207_1512.py
# Compiled at: 2018-02-20 05:54:07
# Size of source mod 2**32: 1055 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_rototalc', '0002_carouselplugin_initial_slide')]
    operations = [
     migrations.AddField(model_name='carouselplugin',
       name='heading_level',
       field=models.PositiveSmallIntegerField(choices=[(1, 'H1'), (2, 'H2'), (3, 'H3'), (4, 'H4'), (5, 'H5'), (6, 'H6')], default=2, help_text='Choose a heading level', verbose_name='heading level')),
     migrations.AddField(model_name='carouselplugin',
       name='subtitle',
       field=models.CharField(blank=True, default='', max_length=400, verbose_name='subtitle')),
     migrations.AddField(model_name='carouselplugin',
       name='title',
       field=models.CharField(blank=True, default='', max_length=400, verbose_name='title'))]