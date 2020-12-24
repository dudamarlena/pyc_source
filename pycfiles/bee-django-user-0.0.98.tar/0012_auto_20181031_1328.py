# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0012_auto_20181031_1328.py
# Compiled at: 2018-10-31 01:28:58
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0011_auto_20181030_1701')]
    operations = [
     migrations.AlterField(model_name=b'userleaverecord', name=b'type', field=models.IntegerField(choices=[(1, '请假'), (2, '请假有销假'), (3, '延期'), (4, '提前')], default=1, verbose_name=b'类型'))]