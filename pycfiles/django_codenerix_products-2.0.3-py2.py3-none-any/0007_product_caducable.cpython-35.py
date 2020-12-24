# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0007_product_caducable.py
# Compiled at: 2018-01-25 02:25:45
# Size of source mod 2**32: 493 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0006_auto_20180118_1126')]
    operations = [
     migrations.AddField(model_name='product', name='caducable', field=models.BooleanField(default=False, verbose_name='Caducable'))]