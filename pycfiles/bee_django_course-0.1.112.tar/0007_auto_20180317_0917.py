# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0007_auto_20180317_0917.py
# Compiled at: 2018-03-17 05:17:27
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0006_auto_20180108_1846')]
    operations = [
     migrations.RemoveField(model_name=b'course', name=b'type_int'),
     migrations.AddField(model_name=b'section', name=b'has_imagework', field=models.BooleanField(default=False, verbose_name=b'是否需要上传图片')),
     migrations.AddField(model_name=b'section', name=b'has_textwork', field=models.BooleanField(default=False, verbose_name=b'是否需要文字作业')),
     migrations.AddField(model_name=b'section', name=b'has_videowork', field=models.BooleanField(default=False, verbose_name=b'是否需要视频录制')),
     migrations.AddField(model_name=b'section', name=b'image_count_req', field=models.IntegerField(default=0, verbose_name=b'要求提交图片数量')),
     migrations.AddField(model_name=b'section', name=b'video_length_req', field=models.IntegerField(default=0, verbose_name=b'要求录制时长(分钟)'))]