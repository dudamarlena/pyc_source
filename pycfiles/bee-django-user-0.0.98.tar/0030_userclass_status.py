# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0030_userclass_status.py
# Compiled at: 2019-08-19 03:31:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0029_auto_20190812_1820')]
    operations = [
     migrations.AddField(model_name=b'userclass', name=b'status', field=models.IntegerField(choices=[(1, '正常'), (2, '已结业')], default=1, verbose_name=b'班级状态'))]