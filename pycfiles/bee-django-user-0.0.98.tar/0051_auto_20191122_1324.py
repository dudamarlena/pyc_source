# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0051_auto_20191122_1324.py
# Compiled at: 2019-11-22 00:24:20
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0050_userleveluprecord_supplement')]
    operations = [
     migrations.AlterField(model_name=b'userleveluprecord', name=b'status', field=models.IntegerField(blank=True, choices=[(-1, '未申请'), (-2, '已申请'), (1, '通过'), (2, '未通过'), (3, '关闭'), (4, '已提交补充资料')], default=-1, null=True, verbose_name=b'状态'))]