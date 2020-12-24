# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/sliders/migrations/0004_sliderimage.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sliders', '0003_remove_slider_pages')]
    operations = [
     migrations.CreateModel(name=b'SliderImage', fields=[
      (
       b'slider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'sliders.Slider'))], options={b'verbose_name': b'Image Slide Show', 
        b'manager_inheritance_from_future': True, 
        b'verbose_name_plural': b'Image Slide Shows'}, bases=('sliders.slider', ))]