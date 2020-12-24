# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0022_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 6338 bytes
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0014_auto_20200316_1110'),
     ('courses', '0021_auto_20190714_1639')]
    operations = [
     migrations.CreateModel(name='CourseFileSegment',
       fields=[
      (
       'basesegment_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='segments.BaseSegment'))],
       options={'verbose_name':'Course File Segment', 
      'verbose_name_plural':'Course Files Segments'},
       bases=('segments.basesegment', )),
     migrations.AlterModelOptions(name='basecourse',
       options={'verbose_name':'Base Course', 
      'verbose_name_plural':'Bases Courses'}),
     migrations.AlterModelOptions(name='course',
       options={'verbose_name':'Course', 
      'verbose_name_plural':'Courses'}),
     migrations.AlterModelOptions(name='coursefile',
       options={'verbose_name':'File', 
      'verbose_name_plural':'Files'}),
     migrations.AlterModelOptions(name='coursesegment',
       options={'verbose_name':'Course Segment', 
      'verbose_name_plural':'Courses Segments'}),
     migrations.AlterModelOptions(name='coursesummary',
       options={'ordering':('id', ), 
      'verbose_name':'Course Summary',  'verbose_name_plural':'Courses Summary'}),
     migrations.AlterField(model_name='basecourse',
       name='description',
       field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description')),
     migrations.AlterField(model_name='course',
       name='banner',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_banner', to='filefields.FileField', verbose_name='Banner Image')),
     migrations.AlterField(model_name='course',
       name='category_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='categories.Category', verbose_name='Category')),
     migrations.AlterField(model_name='course',
       name='cover',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='course_cover', to='filefields.FileField', verbose_name='Cover Image')),
     migrations.AlterField(model_name='course',
       name='dependency_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='dependency', to='courses.Course', verbose_name='Dependency')),
     migrations.AlterField(model_name='course',
       name='parent_obj',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='Parent')),
     migrations.AlterField(model_name='course',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='Publish Date')),
     migrations.AlterField(model_name='course',
       name='publish_day',
       field=models.CharField(blank=True, choices=[('1', 'Saturday'), ('2', 'Sunday'), ('3', 'Monday'), ('4', 'Tuesday'), ('5', 'Wednesday'), ('6', 'Thursday'), ('7', 'Friday')], max_length=1, null=True, verbose_name='DAY')),
     migrations.AlterField(model_name='course',
       name='publish_month',
       field=models.CharField(blank=True, choices=[('1', 'Farvardin'), ('2', 'Ordibehesht'), ('3', 'Khordad'), ('4', 'Tir'), ('5', 'Mordad'), ('6', 'Shahrivar'), ('7', 'Mehr'), ('8', 'Aban'), ('9', 'Azar'), ('10', 'Dey'), ('11', 'Bahman'), ('12', 'Esfand')], max_length=2, null=True, verbose_name='Month')),
     migrations.AlterField(model_name='course',
       name='publish_week',
       field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name='Week')),
     migrations.AlterField(model_name='course',
       name='teacher_obj',
       field=models.ManyToManyField(blank=True, to='teachers.Teacher', verbose_name='Teachers')),
     migrations.AlterField(model_name='coursefile',
       name='course_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='courses.Course', verbose_name='Course')),
     migrations.AlterField(model_name='coursefile',
       name='seconds',
       field=models.BigIntegerField(default=0, verbose_name='Time')),
     migrations.AlterField(model_name='coursesummary',
       name='course',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='total_times', to='courses.BaseCourse', verbose_name='Course')),
     migrations.AlterField(model_name='coursesummary',
       name='file_count',
       field=models.PositiveIntegerField(default=0, verbose_name='File Count')),
     migrations.AlterField(model_name='coursesummary',
       name='file_count_preview',
       field=models.PositiveIntegerField(default=0, verbose_name='File Count Preview')),
     migrations.AlterField(model_name='coursesummary',
       name='total_time_seconds',
       field=models.BigIntegerField(default=0, verbose_name='Time')),
     migrations.AlterField(model_name='coursesummary',
       name='type',
       field=models.CharField(choices=[('M', 'Movie'), ('V', 'Voice'), ('P', 'PDF'), ('I', 'Image'), ('L', 'Link')], max_length=1, verbose_name='Type'))]