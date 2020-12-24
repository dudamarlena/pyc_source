# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0052_auto_20180911_0934.py
# Compiled at: 2018-09-14 05:16:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0051_auto_20180907_1550')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'has_questionwork', field=models.BooleanField(default=False, verbose_name=b'是否需要回答问题')),
     migrations.AddField(model_name=b'section', name=b'pre_name', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'前缀标题'))]