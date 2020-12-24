# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0067_auto_20190819_1414.py
# Compiled at: 2019-08-19 02:14:00
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0066_auto_20190816_1757')]
    operations = [
     migrations.AlterModelOptions(name=b'usercoursesection', options={b'ordering': [b'-created_at'], b'permissions': [('view_all_usercoursesection', '查看所有学生课件'), ('view_teach_usercoursessection', '查看所教的学生课件'), ('view_child_usercoursesection', '查看亲子学生课件'), ('pass_ucs', '能通过学生课件'), ('close_ucs', '能关闭学生课件'), ('open_ucs', '能开启学生课件'), ('minus_live_mins', '能扣减学生直播时长'), ('review_ucs', '能查看学生作业'), ('score_ucs', '能给学生作业评分')], b'verbose_name': b'course学生课件'}),
     migrations.RenameField(model_name=b'usercoursesection', old_name=b'minus_mins', new_name=b'minus_live_mins')]