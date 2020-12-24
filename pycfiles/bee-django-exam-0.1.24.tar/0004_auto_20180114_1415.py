# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0004_auto_20180114_1415.py
# Compiled at: 2018-01-14 01:15:20
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0003_auto_20180112_1821')]
    operations = [
     migrations.RenameModel(old_name=b'UserExam', new_name=b'UserExamRecord'),
     migrations.RenameField(model_name=b'userexamrecord', old_name=b'grade_title', new_name=b'grade_name')]