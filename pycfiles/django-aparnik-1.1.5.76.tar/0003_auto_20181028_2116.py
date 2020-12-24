# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/teachers/migrations/0003_auto_20181028_2116.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sliders', '0002_slidersegment'),
     ('teachers', '0002_auto_20181026_1301')]
    operations = [
     migrations.RemoveField(model_name=b'teacher', name=b'slider_obj'),
     migrations.AddField(model_name=b'teacher', name=b'slider_segment_obj', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'sliders.SliderSegment', verbose_name=b'Slider Semgent'))]