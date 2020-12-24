# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0030_auto_20190124_1651.py
# Compiled at: 2019-01-24 03:51:38
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0029_gradecertfield_text_height')]
    operations = [
     migrations.AlterField(model_name=b'gradecertfield', name=b'text_align', field=models.CharField(help_text=b'文字在填写区域中的对齐方式', max_length=180, verbose_name=b'文字对齐')),
     migrations.AlterField(model_name=b'gradecertfield', name=b'text_bg_color', field=models.CharField(blank=True, help_text=b'选填', max_length=7, null=True, verbose_name=b'文字区域背景颜色')),
     migrations.AlterField(model_name=b'gradecertfield', name=b'text_width', field=models.IntegerField(help_text=b'文字超出此宽度时，会不显示多出的文字', verbose_name=b'文字区域宽度'))]