# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0004_product_slider_segment_obj.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0003_remove_product_slider_obj'),
     ('sliders', '0002_slidersegment')]
    operations = [
     migrations.AddField(model_name=b'product', name=b'slider_segment_obj', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'products_sliders', to=b'sliders.SliderSegment', verbose_name=b'Slider Segment'))]