# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0010_order_postal_cost_value.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 514 bytes
import aparnik.utils.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0009_orderitem_description')]
    operations = [
     migrations.AddField(model_name='order',
       name='postal_cost_value',
       field=aparnik.utils.fields.PriceField(decimal_places=0, default=0, max_digits=20, verbose_name='Postal Cost'))]