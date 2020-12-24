# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0011_question_course.py
# Compiled at: 2019-04-21 06:31:53
from __future__ import unicode_literals
from django.db import migrations
import django.db.models.deletion, smart_selects.db_fields

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0010_question_section')]
    operations = [
     migrations.AddField(model_name=b'question', name=b'course', field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field=b'section', chained_model_field=b'section', null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course_simple.Course', verbose_name=b'课程'))]