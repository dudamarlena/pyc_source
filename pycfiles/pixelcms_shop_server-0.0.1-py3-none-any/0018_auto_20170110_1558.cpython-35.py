# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0018_auto_20170110_1558.py
# Compiled at: 2017-01-10 09:58:57
# Size of source mod 2**32: 631 bytes
from __future__ import unicode_literals
from django.db import migrations
import django.db.models.deletion, mptt.fields

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0017_auto_20170105_1308')]
    operations = [
     migrations.AlterField(model_name='category', name='parent', field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_subcategories', to='shop.Category', verbose_name='parent'))]