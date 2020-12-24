# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0009_auto_20190421_1752.py
# Compiled at: 2019-04-21 05:52:39
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0008_usersection_started_at')]
    operations = [
     migrations.AlterModelOptions(name=b'course', options={b'ordering': [b'-id'], b'permissions': [('can_manage_course', '可以进入课程管理页'), ('view_all_courses', '可以查看所有课程')]}),
     migrations.AlterModelOptions(name=b'question', options={b'ordering': [b'number'], b'permissions': (('view_question', '可以查看问题列表'), )}),
     migrations.AlterModelOptions(name=b'section', options={b'ordering': [b'number'], b'permissions': [('view_all_sections', '可以查看所有课件')]}),
     migrations.AlterModelOptions(name=b'usercourse', options={b'ordering': [b'-created_at'], b'permissions': [('assign_user_course', '能给学生分配课程')]}),
     migrations.AlterModelOptions(name=b'usersection', options={b'ordering': [b'section__number'], b'permissions': [('pass_ucs', '能通过学生课件'), ('close_ucs', '能关闭学生课件'), ('open_ucs', '能开启学生课件')]})]