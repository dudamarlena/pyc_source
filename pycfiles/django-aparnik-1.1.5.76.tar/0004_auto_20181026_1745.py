# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0004_auto_20181026_1745.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0003_auto_20181026_1131')]
    operations = [
     migrations.AlterModelOptions(name=b'basecourse', options={b'verbose_name': b'دوره پایه', b'verbose_name_plural': b'دوره پایه'}),
     migrations.AlterModelOptions(name=b'course', options={b'verbose_name': b'دوره', b'verbose_name_plural': b'دوره'}),
     migrations.AlterModelOptions(name=b'coursefile', options={b'verbose_name': b'فایل', b'verbose_name_plural': b'فایل ها'}),
     migrations.AlterModelOptions(name=b'coursesegment', options={b'verbose_name': b'بخش دوره', b'verbose_name_plural': b'بخش دوره ها'}),
     migrations.AlterModelOptions(name=b'coursesummary', options={b'verbose_name': b'خلاصه دوره', b'verbose_name_plural': b'خلاصه دوره'}),
     migrations.AlterField(model_name=b'basecourse', name=b'description', field=models.TextField(blank=True, null=True, verbose_name=b'توضیحات')),
     migrations.AlterField(model_name=b'course', name=b'banner', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'course_banner', to=b'filefields.FileField', verbose_name=b'بنر')),
     migrations.AlterField(model_name=b'course', name=b'category_obj', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'categories.Category', verbose_name=b'دسته بندی')),
     migrations.AlterField(model_name=b'course', name=b'cover', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'course_cover', to=b'filefields.FileField', verbose_name=b'تصویر جلد')),
     migrations.AlterField(model_name=b'course', name=b'dependency_obj', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'dependency', to=b'courses.Course', verbose_name=b'وابستگی')),
     migrations.AlterField(model_name=b'course', name=b'is_free', field=models.BooleanField(default=False, verbose_name=b'رایگان؟')),
     migrations.AlterField(model_name=b'course', name=b'parent_obj', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'courses.Course', verbose_name=b'والد')),
     migrations.AlterField(model_name=b'course', name=b'publish_date', field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'تاریخ انتشار')),
     migrations.AlterField(model_name=b'course', name=b'publish_day', field=models.CharField(blank=True, choices=[('1', 'شنبه'), ('2', 'یکشنبه'), ('3', 'دوشنبه'), ('4', 'سه شنبه'), ('5', 'چهارشنبه'), ('6', 'پنج شنبه'), ('7', 'جمعه')], max_length=1, null=True, verbose_name=b'روز')),
     migrations.AlterField(model_name=b'course', name=b'publish_month', field=models.CharField(blank=True, choices=[('1', 'فروردین'), ('2', 'اردیبهشت'), ('3', 'خرداد'), ('4', 'تیر'), ('5', 'مرداد'), ('6', 'شهریور'), ('7', 'مهر'), ('8', 'آبان'), ('9', 'آذر'), ('10', 'دی'), ('11', 'بهمن'), ('12', 'اسفند')], max_length=2, null=True, verbose_name=b'ماه')),
     migrations.AlterField(model_name=b'course', name=b'publish_week', field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True, verbose_name=b'هفته')),
     migrations.AlterField(model_name=b'course', name=b'sort', field=models.IntegerField(default=0, verbose_name=b'مرتب سازی')),
     migrations.AlterField(model_name=b'course', name=b'teacher_obj', field=models.ManyToManyField(blank=True, to=b'teachers.Teacher', verbose_name=b'مدرسین')),
     migrations.AlterField(model_name=b'coursefile', name=b'course_obj', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'courses.Course', verbose_name=b'دوره')),
     migrations.AlterField(model_name=b'coursefile', name=b'sort', field=models.IntegerField(default=0, verbose_name=b'مرتب سازی')),
     migrations.AlterField(model_name=b'coursesummary', name=b'course', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'total_times', to=b'courses.BaseCourse', verbose_name=b'دوره')),
     migrations.AlterField(model_name=b'coursesummary', name=b'file_count', field=models.PositiveIntegerField(default=0, verbose_name=b'تعداد فایل ها')),
     migrations.AlterField(model_name=b'coursesummary', name=b'file_count_preview', field=models.PositiveIntegerField(default=0, verbose_name=b'تعداد فایل های پیش نمایش')),
     migrations.AlterField(model_name=b'coursesummary', name=b'type', field=models.CharField(choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس')], max_length=1, verbose_name=b'نوع'))]