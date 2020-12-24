# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0022_sectionvideo.py
# Compiled at: 2018-04-01 07:32:39
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0021_auto_20180328_1554')]
    operations = [
     migrations.CreateModel(name=b'SectionVideo', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section', verbose_name=b'关联的课件')),
      (
       b'video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Video', verbose_name=b'关联的视频'))])]