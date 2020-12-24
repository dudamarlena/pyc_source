# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/sliders/migrations/0004_sliderimage.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 841 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sliders', '0003_remove_slider_pages')]
    operations = [
     migrations.CreateModel(name='SliderImage',
       fields=[
      (
       'slider_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='sliders.Slider'))],
       options={'verbose_name':'Image Slide Show', 
      'manager_inheritance_from_future':True, 
      'verbose_name_plural':'Image Slide Shows'},
       bases=('sliders.slider', ))]