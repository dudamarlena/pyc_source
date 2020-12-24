# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0002_auto_20181203_1533.py
# Compiled at: 2018-12-03 11:15:34
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'voucher', name=b'order_item_obj', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name=b'voucher_order_item', to=b'orders.OrderItem', verbose_name=b'Order Item'))]