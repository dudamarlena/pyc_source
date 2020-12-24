# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0016_category_thumbnail.py
# Compiled at: 2017-01-04 18:08:58
# Size of source mod 2**32: 533 bytes
from __future__ import unicode_literals
from django.db import migrations
import filebrowser.fields

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0015_cart_timestamp')]
    operations = [
     migrations.AddField(model_name='category', name='thumbnail', field=filebrowser.fields.FileBrowseField(blank=True, max_length=255, null=True, verbose_name='thumbnail'))]