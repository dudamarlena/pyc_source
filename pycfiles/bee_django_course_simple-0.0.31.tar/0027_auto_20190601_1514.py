# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0027_auto_20190601_1514.py
# Compiled at: 2019-06-01 03:14:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0026_auto_20190601_1511')]
    operations = [
     migrations.AlterField(model_name=b'question', name=b'score', field=models.IntegerField(blank=True, default=0, null=True, verbose_name=b'答对后得分'))]