# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0014_auto_20180322_1313.py
# Compiled at: 2018-03-22 01:13:59
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0013_auto_20180322_1240')]
    operations = [
     migrations.CreateModel(name=b'UserAssignment', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'content', models.TextField(blank=True, null=True, verbose_name=b'正文')),
      (
       b'work_time', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'总共练习时间')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'score', models.IntegerField(blank=True, null=True, verbose_name=b'得分')),
      (
       b'updated_at', models.DateTimeField(blank=True, null=True)),
      (
       b'submit_at', models.DateTimeField(blank=True, null=True)),
      (
       b'status', models.IntegerField(default=0)),
      (
       b'comment', models.TextField(blank=True, null=True, verbose_name=b'评语')),
      (
       b'reviewed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'rejected_at', models.DateTimeField(blank=True, null=True))]),
     migrations.CreateModel(name=b'UserAssignmentImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'image', models.ImageField(upload_to=b'images/%Y/%m/%d', verbose_name=b'图片作业')),
      (
       b'upload_at', models.DateTimeField(auto_now_add=True, verbose_name=b'上传时间')),
      (
       b'user_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserAssignment'))]),
     migrations.RemoveField(model_name=b'userassignmenttext', name=b'user_course_section'),
     migrations.RemoveField(model_name=b'usercoursesection', name=b'work_time'),
     migrations.DeleteModel(name=b'UserAssignmentText'),
     migrations.AddField(model_name=b'userassignment', name=b'user_course_section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourseSection'))]