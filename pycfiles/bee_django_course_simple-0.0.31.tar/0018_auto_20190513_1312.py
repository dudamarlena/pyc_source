# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0018_auto_20190513_1312.py
# Compiled at: 2019-05-13 01:12:07
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0017_auto_20190510_1710')]
    operations = [
     migrations.AddField(model_name=b'part', name=b'extra_title', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'额外标题')),
     migrations.AddField(model_name=b'section', name=b'extra_title', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'额外标题')),
     migrations.AlterField(model_name=b'part', name=b'pre_title', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'标题前缀')),
     migrations.AlterField(model_name=b'section', name=b'pre_title', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'标题前缀'))]