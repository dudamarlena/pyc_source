# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0006_auto_20190418_1318.py
# Compiled at: 2019-04-18 01:18:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0005_userimage')]
    operations = [
     migrations.AddField(model_name=b'userimage', name=b'model_id', field=models.IntegerField(null=True)),
     migrations.AddField(model_name=b'userimage', name=b'model_name', field=models.CharField(max_length=180, null=True, verbose_name=b'model名')),
     migrations.AlterField(model_name=b'userimage', name=b'image', field=models.ImageField(upload_to=b'bee_django_course_simple/video_image/%Y/%m/%d', verbose_name=b'图片'))]