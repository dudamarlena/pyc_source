# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0029_gradecertfield_text_height.py
# Compiled at: 2019-01-24 02:33:03
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0028_auto_20181219_2057')]
    operations = [
     migrations.AddField(model_name=b'gradecertfield', name=b'text_height', field=models.IntegerField(blank=True, help_text=b'单行文字时可不填写，多行文字时必填', null=True, verbose_name=b'文字区域高度'))]