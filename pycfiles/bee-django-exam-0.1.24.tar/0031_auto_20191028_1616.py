# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0031_auto_20191028_1616.py
# Compiled at: 2019-10-28 04:16:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0030_auto_20190124_1651')]
    operations = [
     migrations.AddField(model_name=b'grade', name=b'subtitle', field=models.CharField(max_length=180, null=True, verbose_name=b'证书显示名称')),
     migrations.AlterField(model_name=b'grade', name=b'order_by', field=models.IntegerField(blank=True, default=0, unique=True, verbose_name=b'顺序'))]