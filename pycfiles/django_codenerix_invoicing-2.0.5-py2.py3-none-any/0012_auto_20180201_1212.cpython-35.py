# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0012_auto_20180201_1212.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 1758 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0009_auto_20180201_1137'),
     ('codenerix_invoicing', '0011_reasonmodificationlinealbaran_reasonmodificationlinebasket_reasonmodificationlineinvoice_reasonmodif')]
    operations = [
     migrations.AddField(model_name='saleslines', name='tax_basket_fk', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lines_sales_basket', to='codenerix_products.TypeTax', verbose_name='Tax Basket'), preserve_default=False),
     migrations.AddField(model_name='saleslines', name='tax_invoice_fk', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lines_sales_invoice', to='codenerix_products.TypeTax', verbose_name='Tax Invoice')),
     migrations.AddField(model_name='saleslines', name='tax_order_fk', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lines_sales_order', to='codenerix_products.TypeTax', verbose_name='Tax Sales order')),
     migrations.AddField(model_name='saleslines', name='tax_ticket_fk', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lines_sales_ticket', to='codenerix_products.TypeTax', verbose_name='Tax Ticket'))]