# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0031_userclass_passed_at.py
# Compiled at: 2019-08-29 02:35:42
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0030_userclass_status')]
    operations = [
     migrations.AddField(model_name=b'userclass', name=b'passed_at', field=models.DateTimeField(null=True, verbose_name=b'结业时间'))]