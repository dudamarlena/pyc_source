# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0005_auto_20190130_1510.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
import datetime
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0009_orderitem_description'),
     ('vouchers', '0004_auto_20190129_1728')]
    operations = [
     migrations.CreateModel(name=b'VoucherOrderItem', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'quantity_usage', models.IntegerField(default=0, verbose_name=b'Quantity Usage')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created at')),
      (
       b'update_at', models.DateTimeField(auto_now=True, verbose_name=b'Update at')),
      (
       b'item_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'voucher_item_spent', to=b'orders.OrderItem', verbose_name=b'Item Spent'))], options={b'verbose_name': b'Voucher Order Item', 
        b'verbose_name_plural': b'Voucher Order Items'}),
     migrations.AddField(model_name=b'voucher', name=b'quantity_remain', field=models.PositiveIntegerField(default=0, verbose_name=b'Quantity Remain')),
     migrations.AlterField(model_name=b'voucher', name=b'expire_at', field=models.DateTimeField(default=datetime.datetime(2219, 1, 30, 15, 10, 1, 32186), verbose_name=b'Expire at')),
     migrations.AddField(model_name=b'voucherorderitem', name=b'voucher_obj', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'voucher_model', to=b'vouchers.Voucher', verbose_name=b'Voucher')),
     migrations.AddField(model_name=b'voucher', name=b'order_item_obj_spent', field=models.ManyToManyField(related_name=b'voucher_order_item_spent', through=b'vouchers.VoucherOrderItem', to=b'orders.OrderItem', verbose_name=b'Item Spent this voucher'))]