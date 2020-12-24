# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0019_auto_20180326_1311.py
# Compiled at: 2018-03-28 03:58:28
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0018_auto_20180324_1703')]
    operations = [
     migrations.AlterField(model_name=b'userassignmentimage', name=b'image', field=models.ImageField(upload_to=b'assignments/%Y/%m/%d', verbose_name=b'图片作业')),
     migrations.AlterField(model_name=b'userassignmentimage', name=b'user_assignment', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserAssignment'))]