# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0051_auto_20180907_1550.py
# Compiled at: 2018-09-07 03:50:33
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0050_sectionquestion_options')]
    operations = [
     migrations.AddField(model_name=b'sectionquestion', name=b'tip_correct', field=models.TextField(null=True, verbose_name=b'正确时提示词')),
     migrations.AddField(model_name=b'sectionquestion', name=b'tip_wrong', field=models.TextField(null=True, verbose_name=b'错误时提示词'))]