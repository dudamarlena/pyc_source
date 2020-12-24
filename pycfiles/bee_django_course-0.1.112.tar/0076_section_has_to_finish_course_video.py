# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0076_section_has_to_finish_course_video.py
# Compiled at: 2019-10-22 02:21:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0075_auto_20191012_1555')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'has_to_finish_course_video', field=models.BooleanField(default=False, verbose_name=b'是否需要看完课件所有视频'))]