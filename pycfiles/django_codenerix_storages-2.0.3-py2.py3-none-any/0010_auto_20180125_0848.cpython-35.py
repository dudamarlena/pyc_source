# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0010_auto_20180125_0848.py
# Compiled at: 2018-01-25 02:48:28
# Size of source mod 2**32: 1518 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0009_auto_20180119_1034')]
    operations = [
     migrations.AddField(model_name='inventoryline', name='caducity', field=models.DateField(blank=True, default=None, null=True, verbose_name='Caducity')),
     migrations.AddField(model_name='inventoryline', name='product_unique_value', field=models.CharField(blank=True, default=None, editable=False, max_length=80, null=True, verbose_name='Product Unique Value')),
     migrations.AlterField(model_name='inventory', name='end', field=models.DateTimeField(blank=True, null=True, verbose_name='Ends')),
     migrations.AlterField(model_name='inventory', name='start', field=models.DateTimeField(blank=True, null=True, verbose_name='Starts')),
     migrations.AlterField(model_name='inventoryline', name='product_unique', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='storage_inventorylines', to='codenerix_products.ProductUnique', verbose_name='Product Unique'))]