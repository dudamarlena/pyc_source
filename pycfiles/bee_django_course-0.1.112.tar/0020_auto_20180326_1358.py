# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0020_auto_20180326_1358.py
# Compiled at: 2018-03-28 03:58:28
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0019_auto_20180326_1311')]
    operations = [
     migrations.RemoveField(model_name=b'userassignmentimage', name=b'user_assignment'),
     migrations.AddField(model_name=b'userassignmentimage', name=b'user_course_section', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserCourseSection'))]