# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0008_auto_20180114_1558.py
# Compiled at: 2018-01-14 02:58:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0007_userexamrecord_passed_date')]
    operations = [
     migrations.AlterField(model_name=b'userexamrecord', name=b'is_passed', field=models.BooleanField(default=False, verbose_name=b'是否通过'))]