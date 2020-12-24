# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0024_userpart_question_correct_count.py
# Compiled at: 2019-05-24 07:34:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0023_auto_20190524_1705')]
    operations = [
     migrations.AddField(model_name=b'userpart', name=b'question_correct_count', field=models.IntegerField(default=0, verbose_name=b'答对了几道题'))]