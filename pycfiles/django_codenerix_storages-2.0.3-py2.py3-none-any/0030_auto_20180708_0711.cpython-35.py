# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/searchwally/codenerix_storages/migrations/0030_auto_20180708_0711.py
# Compiled at: 2018-07-08 01:11:00
# Size of source mod 2**32: 656 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0029_auto_20180430_1924')]
    operations = [
     migrations.AlterField(model_name='lineoutgoingalbaran', name='product_unique', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_outgoing_albarans', to='codenerix_products.ProductUnique', verbose_name='Product Unique'))]