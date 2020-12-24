# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0006_auto_20180129_1256.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 2095 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0005_auto_20180129_1211')]
    operations = [
     migrations.RemoveField(model_name='p', name='a'),
     migrations.RemoveField(model_name='p', name='f'),
     migrations.RemoveField(model_name='p', name='p'),
     migrations.RemoveField(model_name='p', name='product_final'),
     migrations.RemoveField(model_name='saleslines', name='price_recommended'),
     migrations.AddField(model_name='saleslines', name='price_recommended_basket', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Recomended price base')),
     migrations.AddField(model_name='saleslines', name='price_recommended_invoice', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Recomended price base')),
     migrations.AddField(model_name='saleslines', name='price_recommended_order', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Recomended price base')),
     migrations.AddField(model_name='saleslines', name='price_recommended_ticket', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Recomended price base')),
     migrations.DeleteModel(name='Al'),
     migrations.DeleteModel(name='Fa'),
     migrations.DeleteModel(name='P'),
     migrations.DeleteModel(name='Pr')]