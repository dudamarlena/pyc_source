# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0017_auto_20180120_1700.py
# Compiled at: 2018-01-20 04:00:37
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0016_auto_20180120_1605')]
    operations = [
     migrations.AlterField(model_name=b'gradecertfield', name=b'text_bg_color', field=models.CharField(blank=True, max_length=7, null=True, verbose_name=b'文字区域背景颜色'))]