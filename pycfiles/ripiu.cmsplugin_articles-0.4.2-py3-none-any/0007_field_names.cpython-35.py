# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0007_field_names.py
# Compiled at: 2020-04-08 06:50:28
# Size of source mod 2**32: 2333 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles', '0006_auto_20180222_1419')]
    operations = [
     migrations.AlterField(model_name='articlepluginmodel', name='header_alignment', field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')], max_length=10, verbose_name='Header alignment')),
     migrations.AlterField(model_name='articlepluginmodel', name='heading_level', field=models.PositiveSmallIntegerField(choices=[(1, 'H1'), (2, 'H2'), (3, 'H3'), (4, 'H4'), (5, 'H5'), (6, 'H6')], default=2, help_text='Choose a heading level', verbose_name='Heading level')),
     migrations.AlterField(model_name='articlepluginmodel', name='subtitle', field=models.CharField(blank=True, default='', max_length=400, verbose_name='Subtitle')),
     migrations.AlterField(model_name='articlepluginmodel', name='title', field=models.CharField(blank=True, default='', max_length=400, verbose_name='Title')),
     migrations.AlterField(model_name='sectionpluginmodel', name='header_alignment', field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right'), ('center', 'Center')], max_length=10, verbose_name='Header alignment')),
     migrations.AlterField(model_name='sectionpluginmodel', name='heading_level', field=models.PositiveSmallIntegerField(choices=[(1, 'H1'), (2, 'H2'), (3, 'H3'), (4, 'H4'), (5, 'H5'), (6, 'H6')], default=2, help_text='Choose a heading level', verbose_name='Heading level')),
     migrations.AlterField(model_name='sectionpluginmodel', name='subtitle', field=models.CharField(blank=True, default='', max_length=400, verbose_name='Subtitle')),
     migrations.AlterField(model_name='sectionpluginmodel', name='title', field=models.CharField(blank=True, default='', max_length=400, verbose_name='Title'))]