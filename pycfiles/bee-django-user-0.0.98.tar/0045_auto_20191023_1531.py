# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0045_auto_20191023_1531.py
# Compiled at: 2019-10-23 03:31:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0044_auto_20191018_1422')]
    operations = [
     migrations.AlterField(model_name=b'userclass', name=b'status', field=models.IntegerField(blank=True, choices=[(1, '正常'), (2, '已结业')], default=1, verbose_name=b'班级状态'))]