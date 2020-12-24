# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/migrations/0011_auto_20190428_1107.py
# Compiled at: 2019-04-28 02:37:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('orders', '0010_order_postal_cost_value')]
    operations = [
     migrations.AddField(model_name=b'order', name=b'is_sync_with_websites', field=models.BooleanField(default=False, verbose_name=b'Is sync with websites')),
     migrations.AlterField(model_name=b'order', name=b'status', field=models.CharField(choices=[('w', 'Waiting'), ('pa', 'Paid'), ('paw', 'Paid by website'), ('c', 'Cancel'), ('co', 'Complete'), ('d', 'Disputed'), ('ch', 'Challenged')], default=b'w', max_length=5, verbose_name=b'Status'))]