# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0016_auto_20180223_1846.py
# Compiled at: 2018-02-23 12:46:14
# Size of source mod 2**32: 847 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0013_salesorderdocument_removed'),
     ('codenerix_storages', '0015_auto_20180219_1229')]
    operations = [
     migrations.RemoveField(model_name='inventoryout', name='order'),
     migrations.AddField(model_name='inventoryout', name='albaran', field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='inventorys', to='codenerix_invoicing.SalesAlbaran', verbose_name='Albaran'), preserve_default=False)]