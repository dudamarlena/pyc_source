# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0013_auto_20180322_1240.py
# Compiled at: 2018-03-22 00:40:26
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0012_remove_section_order_by')]
    operations = [
     migrations.CreateModel(name=b'UserAssignmentText', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'content', models.TextField(blank=True, null=True, verbose_name=b'正文')),
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
     migrations.CreateModel(name=b'UserCourse', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.IntegerField(default=0, verbose_name=b'状态')),
      (
       b'passed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Course')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'UserCourseSection', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'status', models.IntegerField(default=0)),
      (
       b'score', models.IntegerField(blank=True, null=True, verbose_name=b'得分')),
      (
       b'passed_at', models.DateTimeField(blank=True, null=True)),
      (
       b'work_time', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'总共练习时间')),
      (
       b'section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section')),
      (
       b'user_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourse'))]),
     migrations.AddField(model_name=b'userassignmenttext', name=b'user_course_section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourseSection'))]