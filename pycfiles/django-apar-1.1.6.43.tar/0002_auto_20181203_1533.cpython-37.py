# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0002_auto_20181203_1533.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 563 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='voucher',
       name='order_item_obj',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), related_name='voucher_order_item', to='orders.OrderItem', verbose_name='Order Item'))]