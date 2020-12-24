# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0077_auto_20191021_1603.py
# Compiled at: 2019-10-22 02:21:05
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0076_section_has_to_finish_course_video')]
    operations = [
     migrations.CreateModel(name=b'UserCourseSectionVideo', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'finish_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'user_course_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourseSection')),
      (
       b'video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Video'))]),
     migrations.AlterField(model_name=b'section', name=b'has_to_finish_course_video', field=models.BooleanField(default=False, verbose_name=b'是否需要看完课件所有视频(只对七牛云视频有效)'))]