# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0026_auto_20181117_1416.py
# Compiled at: 2018-11-17 01:16:15
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0025_userstartexam')]
    operations = [
     migrations.AlterField(model_name=b'userexamrecord', name=b'status', field=models.IntegerField(blank=True, choices=[(-1, '未报名'), (-2, '已报名'), (1, '通过'), (2, '未通过'), (3, '关闭')], default=-1, null=True, verbose_name=b'状态'))]