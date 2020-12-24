# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0024_grade_coin.py
# Compiled at: 2018-11-16 02:01:38
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0023_userexamrecord_status')]
    operations = [
     migrations.AddField(model_name=b'grade', name=b'coin', field=models.IntegerField(default=0, verbose_name=b'考级消耗M币'))]