# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0015_section_pre_title.py
# Compiled at: 2019-05-10 01:44:09
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0014_course_is_auto_open')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'pre_title', field=models.CharField(max_length=180, null=True, verbose_name=b'名字前缀'))]