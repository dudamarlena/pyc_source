# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0028_auto_20181219_2057.py
# Compiled at: 2018-12-19 07:57:46
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0027_auto_20181117_1635')]
    operations = [
     migrations.AlterModelOptions(name=b'grade', options={b'ordering': [b'order_by'], b'permissions': (('can_manage_exam', '可以进入考级管理页'), ('view_grade_list', '可以查看考级列表'))}),
     migrations.AlterModelOptions(name=b'notice', options={b'ordering': [b'-id'], b'permissions': (('view_notice_list', '可以查看须知列表'), )}),
     migrations.AlterModelOptions(name=b'userexamrecord', options={b'ordering': [b'-created_at'], b'permissions': (('view_all_user_exam_record_list', '可以查看所有学生考级列表'), ('create_cert', '生成证书'))})]