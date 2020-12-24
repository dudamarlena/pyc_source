# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0019_auto_20180125_1125.py
# Compiled at: 2018-01-24 22:25:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0018_userexamrecord_cert')]
    operations = [
     migrations.AddField(model_name=b'userexamrecord', name=b'year', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'年度')),
     migrations.AlterField(model_name=b'gradecertfield', name=b'font_color', field=models.CharField(default=b'#000000', max_length=7, verbose_name=b'字体颜色')),
     migrations.AlterField(model_name=b'gradecertfield', name=b'font_size', field=models.IntegerField(default=20, verbose_name=b'字体大小'))]