# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0006_auto_20180108_1846.py
# Compiled at: 2018-01-08 05:46:38
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0005_auto_20180108_1640')]
    operations = [
     migrations.CreateModel(name=b'Video', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'video_id', models.CharField(max_length=180, null=True)),
      (
       b'status', models.CharField(max_length=180, null=True)),
      (
       b'duration', models.CharField(max_length=180, null=True)),
      (
       b'image', models.CharField(max_length=180, null=True)),
      (
       b'title', models.CharField(max_length=180, null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_course_video'}),
     migrations.AlterModelOptions(name=b'coursesectionmid', options={b'ordering': [b'order_by']}),
     migrations.AddField(model_name=b'section', name=b'videos', field=models.ManyToManyField(to=b'bee_django_course.Video'))]