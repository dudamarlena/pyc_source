# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0013_auto_20181112_1534.py
# Compiled at: 2018-11-12 02:34:42
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0012_auto_20181112_1527')]
    operations = [
     migrations.AlterField(model_name=b'item', name=b'pic', field=models.ImageField(blank=True, null=True, upload_to=b'bee_django_coin/shop/item', verbose_name=b'商品图片'))]