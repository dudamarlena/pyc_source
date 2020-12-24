# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0009_item_order.py
# Compiled at: 2018-11-09 01:04:34
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_coin', '0008_auto_20181019_1557')]
    operations = [
     migrations.CreateModel(name=b'Item', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'商品名称')),
      (
       b'coin', models.IntegerField(verbose_name=b'购买需要')),
      (
       b'pic', models.TextField(help_text=b'目前仅支持网络图片', null=True, verbose_name=b'商品图片网址')),
      (
       b'info', models.TextField(null=True, verbose_name=b'详情')),
      (
       b'item_type', models.IntegerField(default=0, verbose_name=b'商品类型')),
      (
       b'stauts', models.IntegerField(default=0, verbose_name=b'商品状态')),
      (
       b'edit_at', models.DateTimeField(auto_now=True))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_coin_item'}),
     migrations.CreateModel(name=b'Order', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order_id', models.CharField(max_length=180)),
      (
       b'item_id', models.IntegerField()),
      (
       b'item_name', models.CharField(max_length=180)),
      (
       b'item_count', models.IntegerField(default=0)),
      (
       b'item_coin', models.IntegerField(default=0)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.IntegerField(default=1)),
      (
       b'info', models.TextField(null=True, verbose_name=b'备注')),
      (
       b'evaluate', models.IntegerField(null=True)),
      (
       b'evaluate_info', models.TextField(null=True)),
      (
       b'evaluate_datetime', models.DateTimeField(null=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'购买人'))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_coin_order'})]