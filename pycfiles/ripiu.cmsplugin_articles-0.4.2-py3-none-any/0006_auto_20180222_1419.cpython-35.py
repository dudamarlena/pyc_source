# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0006_auto_20180222_1419.py
# Compiled at: 2020-04-08 06:01:34
# Size of source mod 2**32: 1315 bytes
from __future__ import unicode_literals
import djangocms_attributes_field.fields
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles', '0005_auto_20180222_1207')]
    operations = [
     migrations.AddField(model_name='articlepluginmodel', name='attributes', field=djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
     migrations.AddField(model_name='articlepluginmodel', name='template', field=models.CharField(choices=[('default', 'Default')], default='default', max_length=255, verbose_name='Template')),
     migrations.AddField(model_name='sectionpluginmodel', name='attributes', field=djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
     migrations.AddField(model_name='sectionpluginmodel', name='template', field=models.CharField(choices=[('default', 'Default')], default='default', max_length=255, verbose_name='Template'))]