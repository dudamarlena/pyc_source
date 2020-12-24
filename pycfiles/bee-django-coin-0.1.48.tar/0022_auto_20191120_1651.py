# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0022_auto_20191120_1651.py
# Compiled at: 2019-11-20 03:51:08
from __future__ import unicode_literals
import bee_django_richtext.custom_fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0021_order_deliver')]
    operations = [
     migrations.AlterField(model_name=b'item', name=b'info', field=bee_django_richtext.custom_fields.RichTextField(app_name=b'bee_django_coin', blank=True, emotion=False, image_max_size=2, img=True, model_name=b'Item', null=True, text_min_length=5, undo_redo=False, verbose_name=b'详情'))]