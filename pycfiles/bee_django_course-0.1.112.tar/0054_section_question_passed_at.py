# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0054_section_question_passed_at.py
# Compiled at: 2018-09-14 05:16:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0053_section_image')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'question_passed_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'问答通过时间'))]