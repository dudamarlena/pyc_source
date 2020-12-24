# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0029_auto_20191106_1409.py
# Compiled at: 2019-11-06 02:45:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0028_userquestion_is_correct')]
    operations = [
     migrations.AddField(model_name=b'part', name=b'award_name', field=models.CharField(blank=True, help_text=b'仅在小节类型为问题，且有正确答案时显示', max_length=180, null=True, verbose_name=b'奖品名称')),
     migrations.AddField(model_name=b'part', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'说明')),
     migrations.AlterField(model_name=b'question', name=b'tip_correct', field=models.TextField(blank=True, null=True, verbose_name=b'正确时提示词')),
     migrations.AlterField(model_name=b'question', name=b'tip_wrong', field=models.TextField(blank=True, null=True, verbose_name=b'错误时提示词'))]