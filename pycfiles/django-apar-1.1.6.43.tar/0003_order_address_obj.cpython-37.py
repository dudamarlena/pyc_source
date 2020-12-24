# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0003_order_address_obj.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 597 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('addresses', '0001_initial'),
     ('orders', '0002_auto_20181026_1301')]
    operations = [
     migrations.AddField(model_name='order',
       name='address_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='addresses.UserAddress', verbose_name='Order Address'))]