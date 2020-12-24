# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0016_auto_20190510_1652.py
# Compiled at: 2019-05-10 04:52:36
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0015_section_pre_title')]
    operations = [
     migrations.AddField(model_name=b'part', name=b'pre_title', field=models.CharField(max_length=180, null=True, verbose_name=b'标题前缀')),
     migrations.AddField(model_name=b'section', name=b'group_name', field=models.CharField(help_text=b'如课件前不需显示，则不用填写', max_length=180, null=True, verbose_name=b'组名')),
     migrations.AlterField(model_name=b'course', name=b'title', field=models.CharField(max_length=180, verbose_name=b'课程标题')),
     migrations.AlterField(model_name=b'section', name=b'pre_title', field=models.CharField(max_length=180, null=True, verbose_name=b'标题前缀')),
     migrations.AlterField(model_name=b'section', name=b'title', field=models.CharField(max_length=180, verbose_name=b'课件标题'))]