# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0016_purchaseslinealbaran_product_unique.py
# Compiled at: 2018-02-27 03:00:35
# Size of source mod 2**32: 666 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0011_auto_20180202_0826'),
     ('codenerix_invoicing', '0015_remove_purchaseslinealbaran_product_unique')]
    operations = [
     migrations.AddField(model_name='purchaseslinealbaran', name='product_unique', field=models.ManyToManyField(related_name='line_albaran_purchases', to='codenerix_products.ProductUnique', verbose_name='Product Unique'))]