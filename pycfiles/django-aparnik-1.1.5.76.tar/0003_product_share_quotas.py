# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0003_product_share_quotas.py
# Compiled at: 2018-11-02 01:37:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0002_product_is_free')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'share_quotas', field=models.IntegerField(default=0, verbose_name=b'Share Quotas'))]