# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0017_auto_20180324_0915.py
# Compiled at: 2018-03-23 21:15:18
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0016_course_teacher')]
    operations = [
     migrations.AlterField(model_name=b'usercourse', name=b'course', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Course', verbose_name=b'课程'))]