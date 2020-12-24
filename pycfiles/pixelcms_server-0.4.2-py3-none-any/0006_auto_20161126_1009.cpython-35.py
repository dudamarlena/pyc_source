# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/content/migrations/0006_auto_20161126_1009.py
# Compiled at: 2016-11-26 04:09:48
# Size of source mod 2**32: 515 bytes
from __future__ import unicode_literals
from django.db import migrations
import filebrowser.fields

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0005_auto_20161121_0019')]
    operations = [
     migrations.AlterField(model_name='articleimage', name='image', field=filebrowser.fields.FileBrowseField(max_length=255, verbose_name='image'))]