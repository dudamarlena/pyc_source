# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0014_auto_20180227_0858.py
# Compiled at: 2018-02-27 02:58:45
# Size of source mod 2**32: 775 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0011_auto_20180202_0826'),
     ('codenerix_invoicing', '0013_salesorderdocument_removed')]
    operations = [
     migrations.RemoveField(model_name='purchaseslinealbaran', name='product_unique'),
     migrations.AddField(model_name='purchaseslinealbaran', name='product_unique', field=models.ManyToManyField(related_name='line_albaran_purchases', to='codenerix_products.ProductUnique', verbose_name='Product Unique'))]