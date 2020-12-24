# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/content/migrations/0003_auto_20161120_2334.py
# Compiled at: 2016-11-20 17:34:31
# Size of source mod 2**32: 726 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import filebrowser.fields

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0002_auto_20161120_2116')]
    operations = [
     migrations.AddField(model_name='category', name='image', field=filebrowser.fields.FileBrowseField(blank=True, max_length=255, null=True, verbose_name='image')),
     migrations.AddField(model_name='category', name='show_image', field=models.BooleanField(default=True, verbose_name='show image'))]