# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0075_auto_20191012_1555.py
# Compiled at: 2019-10-12 03:55:22
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0074_auto_20191012_1414')]
    operations = [
     migrations.AlterField(model_name=b'course', name=b'punch_period', field=models.IntegerField(blank=True, choices=[(1, '天')], help_text=b'用于课程打卡，如不需要可不填写', null=True, verbose_name=b'周期'))]