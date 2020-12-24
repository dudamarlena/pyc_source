# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0008_auto_20180130_1312.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 932 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0007_auto_20180129_1258')]
    operations = [
     migrations.AlterField(model_name='salesbasket', name='pos', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_sales', to='codenerix_pos.POS', verbose_name='Point of Sales')),
     migrations.AlterField(model_name='salesbasket', name='pos_slot', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_sales', to='codenerix_pos.POSSlot', verbose_name='POS Slot'))]