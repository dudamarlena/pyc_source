# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0015_auto_20180219_1229.py
# Compiled at: 2018-02-19 06:29:19
# Size of source mod 2**32: 682 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0014_inventoryinline_purchasesorder')]
    operations = [
     migrations.AlterField(model_name='inventoryinline', name='purchasesorder', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_lines', to='codenerix_invoicing.PurchasesOrder', verbose_name='Inventory line'))]