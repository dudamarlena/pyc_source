# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0033_auto_20180517_1937.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0032_auto_20180517_1848')]
    operations = [
     migrations.AlterModelOptions(name=b'course', options={b'ordering': [b'-id'], b'permissions': (('can_manage_course', '可以进入课程管理页'), ('view_all_courses', '可以查看所有课程'), ('can_choose_course', 'can choose course')), b'verbose_name': b'course课程'}),
     migrations.AlterModelOptions(name=b'section', options={b'ordering': [b'-id'], b'permissions': (('view_all_sections', '可以查看所有课件'), ), b'verbose_name': b'course课件'}),
     migrations.AlterModelOptions(name=b'usercoursesection', options={b'ordering': [b'-created_at'], b'permissions': [('view_all_usercoursesection', '查看所有学生课件'), ('view_teach_usercoursessection', '查看所教的学生课件')], b'verbose_name': b'course学生课件'}),
     migrations.AlterModelOptions(name=b'userlive', options={b'ordering': [b'-created_at'], b'permissions': (('view_all_userlives', '可以查看所有学生的录播'), ('view_teach_userlives', '可以查看所教的学生的录播')), b'verbose_name': b'course学生录播'}),
     migrations.AlterModelOptions(name=b'video', options={b'ordering': [b'-created_at'], b'permissions': (('view_all_videos', '可以查看所有视频'), ), b'verbose_name': b'course视频'})]