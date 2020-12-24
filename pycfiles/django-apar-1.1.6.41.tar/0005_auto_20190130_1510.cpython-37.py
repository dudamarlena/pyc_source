# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0005_auto_20190130_1510.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2217 bytes
import datetime
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0009_orderitem_description'),
     ('vouchers', '0004_auto_20190129_1728')]
    operations = [
     migrations.CreateModel(name='VoucherOrderItem',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'quantity_usage', models.IntegerField(default=0, verbose_name='Quantity Usage')),
      (
       'created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
      (
       'update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
      (
       'item_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='voucher_item_spent', to='orders.OrderItem', verbose_name='Item Spent'))],
       options={'verbose_name':'Voucher Order Item', 
      'verbose_name_plural':'Voucher Order Items'}),
     migrations.AddField(model_name='voucher',
       name='quantity_remain',
       field=models.PositiveIntegerField(default=0, verbose_name='Quantity Remain')),
     migrations.AlterField(model_name='voucher',
       name='expire_at',
       field=models.DateTimeField(default=(datetime.datetime(2219, 1, 30, 15, 10, 1, 32186)), verbose_name='Expire at')),
     migrations.AddField(model_name='voucherorderitem',
       name='voucher_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='voucher_model', to='vouchers.Voucher', verbose_name='Voucher')),
     migrations.AddField(model_name='voucher',
       name='order_item_obj_spent',
       field=models.ManyToManyField(related_name='voucher_order_item_spent', through='vouchers.VoucherOrderItem', to='orders.OrderItem', verbose_name='Item Spent this voucher'))]