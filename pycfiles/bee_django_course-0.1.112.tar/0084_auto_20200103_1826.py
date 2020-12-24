# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0084_auto_20200103_1826.py
# Compiled at: 2020-01-03 05:26:57
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0083_auto_20191230_1625')]
    operations = [
     migrations.AlterField(model_name=b'usercoursesection', name=b'teacher_add_mins', field=models.IntegerField(blank=True, default=0, verbose_name=b'助教增加的练习时间'))]