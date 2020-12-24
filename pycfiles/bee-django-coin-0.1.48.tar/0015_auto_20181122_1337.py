# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0015_auto_20181122_1337.py
# Compiled at: 2018-11-22 00:37:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0014_item_url')]
    operations = [
     migrations.AlterField(model_name=b'item', name=b'url', field=models.URLField(blank=True, help_text=b'填写此项后，点击该商品则自动跳转到链接地址。', null=True, verbose_name=b'商品链接'))]