# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0002_auto_20181025_1543.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('segments', '0001_initial'),
     ('filefields', '0001_initial'),
     ('teachers', '0001_initial'),
     ('categories', '0001_initial'),
     ('courses', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'CourseSegment', fields=[
      (
       b'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'segments.BaseSegment'))], options={b'verbose_name': b'Course Segment', 
        b'verbose_name_plural': b'Courses Segments'}, bases=('segments.basesegment', )),
     migrations.CreateModel(name=b'CourseSummary', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'total_time_seconds', models.CharField(default=b'0', max_length=255, verbose_name=b'زمان')),
      (
       b'file_count', models.PositiveIntegerField(default=0, verbose_name=b'File Count')),
      (
       b'file_count_preview', models.PositiveIntegerField(default=0, verbose_name=b'File Count Preview')),
      (
       b'type', models.CharField(choices=[('M', 'Movie'), ('V', 'Voice'), ('P', 'PDF'), ('I', 'تصویر')], max_length=1, verbose_name=b'Type'))], options={b'verbose_name': b'Course Summary', 
        b'verbose_name_plural': b'Courses Summary'}),
     migrations.CreateModel(name=b'Course', fields=[
      (
       b'basecourse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'courses.BaseCourse')),
      (
       b'sort', models.IntegerField(default=0, verbose_name=b'Sort')),
      (
       b'is_free', models.BooleanField(default=False, verbose_name=b'Is Free')),
      (
       b'publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Publish Date')),
      (
       b'publish_month', models.CharField(blank=True, choices=[('1', 'Farvardin'), ('2', 'Ordibehesht'), ('3', 'Khordad'), ('4', 'Tir'), ('5', 'Mordad'), ('6', 'Shahrivar'), ('7', 'Mehr'), ('8', 'Aban'), ('9', 'Azar'), ('10', 'Dey'), ('11', 'Bahman'), ('12', 'Esfand')], max_length=2, null=True, verbose_name=b'Month')),
      (
       b'publish_week', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name=b'Week')),
      (
       b'publish_day', models.CharField(blank=True, choices=[('1', 'شنبه'), ('2', 'یکشنبه'), ('3', 'دوشنبه'), ('4', 'سه شنبه'), ('5', 'چهارشنبه'), ('6', 'پنجشنبه'), ('7', 'جمعه')], max_length=1, null=True, verbose_name=b'DAY')),
      (
       b'banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'course_banner', to=b'filefields.FileField', verbose_name=b'Banner Image')),
      (
       b'category_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'categories.Category', verbose_name=b'Category')),
      (
       b'cover', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'course_cover', to=b'filefields.FileField', verbose_name=b'Cover Image')),
      (
       b'dependency_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'dependency', to=b'courses.Course', verbose_name=b'Dependency')),
      (
       b'parent_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'courses.Course', verbose_name=b'Parent')),
      (
       b'teacher_obj', models.ManyToManyField(blank=True, null=True, to=b'teachers.Teacher', verbose_name=b'Teachers'))], options={b'verbose_name': b'Course', 
        b'verbose_name_plural': b'Courses'}, bases=('courses.basecourse', )),
     migrations.AddField(model_name=b'coursesummary', name=b'course', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'total_times', to=b'courses.BaseCourse', verbose_name=b'Course')),
     migrations.AddField(model_name=b'coursefile', name=b'course_obj', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'courses.Course', verbose_name=b'Course'))]