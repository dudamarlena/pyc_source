# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0007_auto_20181026_1751.py
# Compiled at: 2018-10-26 05:51:25
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0006_userleaverecord')]
    operations = [
     migrations.AlterField(model_name=b'userleaverecord', name=b'old_expire', field=models.DateTimeField(blank=True, null=True, verbose_name=b'原结课日期')),
     migrations.AlterField(model_name=b'userleaverecord', name=b'type', field=models.IntegerField(choices=[(1, '请假'), (2, '销假'), (3, '延期')], default=1, verbose_name=b'类型'))]