# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0004_auto_20180108_1638.py
# Compiled at: 2018-01-08 03:38:10
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0003_section')]
    operations = [
     migrations.CreateModel(name=b'CourseSectionMid', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'order_by', models.IntegerField(default=0, verbose_name=b'顺序')),
      (
       b'mins', models.IntegerField(blank=True, null=True, verbose_name=b'达标分钟数')),
      (
       b'course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Course', verbose_name=b'课程'))], options={b'db_table': b'course_section_mid'}),
     migrations.AlterField(model_name=b'section', name=b'info', field=models.CharField(max_length=180, null=True, verbose_name=b'说明')),
     migrations.AlterField(model_name=b'section', name=b'name', field=models.CharField(max_length=180, verbose_name=b'课件名字')),
     migrations.AlterField(model_name=b'section', name=b'order_by', field=models.IntegerField(null=True, verbose_name=b'课件排序')),
     migrations.AddField(model_name=b'coursesectionmid', name=b'section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section', verbose_name=b'课件'))]