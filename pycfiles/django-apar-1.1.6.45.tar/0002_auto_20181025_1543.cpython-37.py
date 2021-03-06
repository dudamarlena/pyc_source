# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0002_auto_20181025_1543.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 5152 bytes
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
     migrations.CreateModel(name='CourseSegment',
       fields=[
      (
       'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='segments.BaseSegment'))],
       options={'verbose_name':'Course Segment', 
      'verbose_name_plural':'Courses Segments'},
       bases=('segments.basesegment', )),
     migrations.CreateModel(name='CourseSummary',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'total_time_seconds', models.CharField(default='0', max_length=255, verbose_name='\\u0632\\u0645\\u0627\\u0646')),
      (
       'file_count', models.PositiveIntegerField(default=0, verbose_name='File Count')),
      (
       'file_count_preview', models.PositiveIntegerField(default=0, verbose_name='File Count Preview')),
      (
       'type', models.CharField(choices=[('M', 'Movie'), ('V', 'Voice'), ('P', 'PDF'), ('I', '\\u062a\\u0635\\u0648\\u06cc\\u0631')], max_length=1, verbose_name='Type'))],
       options={'verbose_name':'Course Summary', 
      'verbose_name_plural':'Courses Summary'}),
     migrations.CreateModel(name='Course',
       fields=[
      (
       'basecourse_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='courses.BaseCourse')),
      (
       'sort', models.IntegerField(default=0, verbose_name='Sort')),
      (
       'is_free', models.BooleanField(default=False, verbose_name='Is Free')),
      (
       'publish_date', models.DateTimeField(default=(django.utils.timezone.now), verbose_name='Publish Date')),
      (
       'publish_month', models.CharField(blank=True, choices=[('1', 'Farvardin'), ('2', 'Ordibehesht'), ('3', 'Khordad'), ('4', 'Tir'), ('5', 'Mordad'), ('6', 'Shahrivar'), ('7', 'Mehr'), ('8', 'Aban'), ('9', 'Azar'), ('10', 'Dey'), ('11', 'Bahman'), ('12', 'Esfand')], max_length=2, null=True, verbose_name='Month')),
      (
       'publish_week', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name='Week')),
      (
       'publish_day', models.CharField(blank=True, choices=[('1', '\\u0634\\u0646\\u0628\\u0647'), ('2', '\\u06cc\\u06a9\\u0634\\u0646\\u0628\\u0647'), ('3', '\\u062f\\u0648\\u0634\\u0646\\u0628\\u0647'), ('4', '\\u0633\\u0647 \\u0634\\u0646\\u0628\\u0647'), ('5', '\\u0686\\u0647\\u0627\\u0631\\u0634\\u0646\\u0628\\u0647'), ('6', '\\u067e\\u0646\\u062c\\u0634\\u0646\\u0628\\u0647'), ('7', '\\u062c\\u0645\\u0639\\u0647')], max_length=1, null=True, verbose_name='DAY')),
      (
       'banner', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_banner', to='filefields.FileField', verbose_name='Banner Image')),
      (
       'category_obj', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='categories.Category', verbose_name='Category')),
      (
       'cover', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_cover', to='filefields.FileField', verbose_name='Cover Image')),
      (
       'dependency_obj', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='dependency', to='courses.Course', verbose_name='Dependency')),
      (
       'parent_obj', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='Parent')),
      (
       'teacher_obj', models.ManyToManyField(blank=True, null=True, to='teachers.Teacher', verbose_name='Teachers'))],
       options={'verbose_name':'Course', 
      'verbose_name_plural':'Courses'},
       bases=('courses.basecourse', )),
     migrations.AddField(model_name='coursesummary',
       name='course',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='total_times', to='courses.BaseCourse', verbose_name='Course')),
     migrations.AddField(model_name='coursefile',
       name='course_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='Course'))]