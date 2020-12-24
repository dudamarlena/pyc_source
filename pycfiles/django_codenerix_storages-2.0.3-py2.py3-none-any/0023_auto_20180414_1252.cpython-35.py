# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0023_auto_20180414_1252.py
# Compiled at: 2018-04-14 06:52:48
# Size of source mod 2**32: 772 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0017_cashdiary_cashmovement'),
     ('codenerix_storages', '0022_auto_20180414_0607')]
    operations = [
     migrations.RemoveField(model_name='inventoryinline', name='purchaseslinealbaran'),
     migrations.AddField(model_name='inventoryinline', name='purchaseslinealbaran', field=models.ManyToManyField(related_name='inventory_lines', to='codenerix_invoicing.PurchasesLineAlbaran', verbose_name='Line Albaran'))]