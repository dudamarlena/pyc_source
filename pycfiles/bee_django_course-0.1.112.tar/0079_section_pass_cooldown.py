# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0079_section_pass_cooldown.py
# Compiled at: 2019-10-29 04:10:58
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0078_auto_20191023_1625')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'pass_cooldown', field=models.IntegerField(default=0, help_text=b'通过时距离上一课件的间隔天数', verbose_name=b'间隔天数'))]