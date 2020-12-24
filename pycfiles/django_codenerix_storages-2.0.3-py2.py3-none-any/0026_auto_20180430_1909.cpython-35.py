# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0026_auto_20180430_1909.py
# Compiled at: 2018-04-30 13:09:53
# Size of source mod 2**32: 1104 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0025_auto_20180426_1035')]
    operations = [
     migrations.RemoveField(model_name='lineoutgoingalbaran', name='prepare_user'),
     migrations.AddField(model_name='outgoingalbaran', name='inventory', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outgoing_albarans', to='codenerix_storages.InventoryOut', verbose_name='Inventory')),
     migrations.AlterField(model_name='outgoingalbaran', name='request_stock', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_albarans', to='codenerix_storages.RequestStock', verbose_name='Request stock'))]