# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/migrations/0007_auto_20161230_2117.py
# Compiled at: 2016-12-30 15:17:37
# Size of source mod 2**32: 481 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('shop', '0006_auto_20161230_1907')]
    operations = [
     migrations.AlterField(model_name='cartproduct', name='quantity', field=models.PositiveSmallIntegerField(verbose_name='quantity'))]