# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/migrations/0005_auto_20180222_1207.py
# Compiled at: 2018-02-22 06:07:47
# Size of source mod 2**32: 1034 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles', '0004_auto_20171213_1327')]
    operations = [
     migrations.RemoveField(model_name='articlepluginmodel', name='alignment'),
     migrations.RemoveField(model_name='articlepluginmodel', name='featured_image'),
     migrations.RemoveField(model_name='articlepluginmodel', name='thumbnail_option'),
     migrations.RemoveField(model_name='sectionpluginmodel', name='alignment'),
     migrations.RemoveField(model_name='sectionpluginmodel', name='featured_image'),
     migrations.RemoveField(model_name='sectionpluginmodel', name='thumbnail_option')]