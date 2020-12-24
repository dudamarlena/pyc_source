# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0004_auto_20190417_1737.py
# Compiled at: 2019-04-17 05:37:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0003_auto_20190416_1737')]
    operations = [
     migrations.RemoveField(model_name=b'video', name=b'url'),
     migrations.AddField(model_name=b'video', name=b'file_name', field=models.CharField(default=b'', max_length=180, verbose_name=b'视频文件名'), preserve_default=False)]