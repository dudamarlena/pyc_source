# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0001_initial.py
# Compiled at: 2019-04-16 04:13:42
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Course', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'课程名字')),
      (
       b'subtitle', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'课程副标题')),
      (
       b'level', models.IntegerField(blank=True, default=0, verbose_name=b'课程的level')),
      (
       b'is_del', models.IntegerField(default=0)),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_course_simple_course', 
        b'verbose_name': b'course课程'}),
     migrations.CreateModel(name=b'Option', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'选项')),
      (
       b'number', models.IntegerField(default=0, verbose_name=b'顺序')),
      (
       b'is_correct', models.BooleanField(default=False, verbose_name=b'是否正确答案'))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_course_simple_option'}),
     migrations.CreateModel(name=b'Part', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'标题')),
      (
       b'number', models.IntegerField(default=1, verbose_name=b'排序')),
      (
       b'type', models.IntegerField(default=1, verbose_name=b'类型')),
      (
       b'has_answer', models.BooleanField(default=False, verbose_name=b'是否有正确答案'))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_course_simple_part', 
        b'verbose_name': b'小节'}),
     migrations.CreateModel(name=b'Question', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'number', models.IntegerField(default=1, verbose_name=b'排序')),
      (
       b'title', models.CharField(max_length=180, null=True, verbose_name=b'问题')),
      (
       b'tip_wrong', models.TextField(null=True, verbose_name=b'错误时提示词')),
      (
       b'tip_correct', models.TextField(null=True, verbose_name=b'正确时提示词')),
      (
       b'part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Part', verbose_name=b'小节'))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_course_simple_question'}),
     migrations.CreateModel(name=b'Section', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'课件名字')),
      (
       b'number', models.IntegerField(default=1, verbose_name=b'排序')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'介绍')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Course', verbose_name=b'属于的课程'))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_course_simple_section', 
        b'verbose_name': b'course课件'}),
     migrations.CreateModel(name=b'Video', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'number', models.IntegerField(default=1, verbose_name=b'排序')),
      (
       b'content', models.TextField(verbose_name=b'内容')),
      (
       b'part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Part', verbose_name=b'小节')),
      (
       b'url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Question', verbose_name=b'视频地址'))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_course_simple_video'}),
     migrations.AddField(model_name=b'part', name=b'section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Section', verbose_name=b'属于的课件')),
     migrations.AddField(model_name=b'option', name=b'question', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Question', verbose_name=b'问题'))]