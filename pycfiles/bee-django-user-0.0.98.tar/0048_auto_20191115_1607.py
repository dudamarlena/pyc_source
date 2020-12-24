# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0048_auto_20191115_1607.py
# Compiled at: 2019-11-15 03:07:52
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0047_userclassremoverecord')]
    operations = [
     migrations.AlterField(model_name=b'userclass', name=b'name', field=models.CharField(help_text=b'不能和已有班级重名', max_length=180, unique=True, verbose_name=b'班级名称'))]