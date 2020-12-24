# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0005_auto_20181108_1132.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0004_product_slider_segment_obj')]
    operations = [
     migrations.RenameField(model_name=b'product', old_name=b'discount_percent', new_name=b'discount_percent_value'),
     migrations.AddField(model_name=b'product', name=b'discount_percent_expire', field=models.DateTimeField(blank=True, help_text=b'If blank, without expire', null=True, verbose_name=b'Discount Expire')),
     migrations.AddField(model_name=b'product', name=b'is_discount_percent_expire_show', field=models.BooleanField(default=False, help_text=b'If True countdown is available', verbose_name=b'Is Discount Expire Show'))]