# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0007_auto_20180129_1258.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 1777 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0006_auto_20180129_1256')]
    operations = [
     migrations.AlterField(model_name='saleslines', name='discount_invoice', field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Discount (%)')),
     migrations.AlterField(model_name='saleslines', name='discount_order', field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Discount (%)')),
     migrations.AlterField(model_name='saleslines', name='discount_ticket', field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Discount (%)')),
     migrations.AlterField(model_name='saleslines', name='price_base_invoice', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price base')),
     migrations.AlterField(model_name='saleslines', name='price_base_order', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price base')),
     migrations.AlterField(model_name='saleslines', name='price_base_ticket', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price base'))]