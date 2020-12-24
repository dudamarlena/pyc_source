# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0012_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 532 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0011_auto_20190428_1107')]
    operations = [
     migrations.AlterField(model_name='orderitem',
       name='product_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='orderitem_set', to='products.Product', verbose_name='Product'))]