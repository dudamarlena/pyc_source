# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0005_auto_20181108_1132.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 948 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0004_product_slider_segment_obj')]
    operations = [
     migrations.RenameField(model_name='product',
       old_name='discount_percent',
       new_name='discount_percent_value'),
     migrations.AddField(model_name='product',
       name='discount_percent_expire',
       field=models.DateTimeField(blank=True, help_text='If blank, without expire', null=True, verbose_name='Discount Expire')),
     migrations.AddField(model_name='product',
       name='is_discount_percent_expire_show',
       field=models.BooleanField(default=False, help_text='If True countdown is available', verbose_name='Is Discount Expire Show'))]