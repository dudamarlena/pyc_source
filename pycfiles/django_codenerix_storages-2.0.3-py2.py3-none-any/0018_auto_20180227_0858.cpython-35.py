# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0018_auto_20180227_0858.py
# Compiled at: 2018-02-27 02:58:45
# Size of source mod 2**32: 1470 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0014_auto_20180227_0858'),
     ('codenerix_storages', '0017_inventoryoutline_caducity')]
    operations = [
     migrations.RemoveField(model_name='inventoryoutline', name='caducity'),
     migrations.AddField(model_name='inventoryinline', name='purchaseslinealbaran', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_lines', to='codenerix_invoicing.PurchasesLineAlbaran', verbose_name='Line Albaran')),
     migrations.AlterField(model_name='inventoryinline', name='inventory', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_lines', to='codenerix_storages.InventoryIn', verbose_name='Inventory')),
     migrations.AlterField(model_name='inventoryinline', name='purchasesorder', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_lines', to='codenerix_invoicing.PurchasesOrder', verbose_name='Order'))]