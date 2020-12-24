# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_pos/migrations/0002_auto_20180118_1458.py
# Compiled at: 2018-01-18 10:17:33
# Size of source mod 2**32: 615 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_pos', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='posproduct', name='group_product', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posproducts', to='codenerix_pos.POSGroupProduct', verbose_name='Group Product'))]