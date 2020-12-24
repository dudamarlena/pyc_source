# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0014_item_url.py
# Compiled at: 2018-11-22 00:35:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0013_auto_20181112_1534')]
    operations = [
     migrations.AddField(model_name=b'item', name=b'url', field=models.URLField(blank=True, help_text=b'填写此项后，点击该商品则自动调整到链接地址。', null=True, verbose_name=b'商品链接'))]