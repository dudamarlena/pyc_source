# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0027_auto_20181117_1635.py
# Compiled at: 2018-11-17 03:35:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0026_auto_20181117_1416')]
    operations = [
     migrations.AlterField(model_name=b'notice', name=b'is_require', field=models.BooleanField(default=True, verbose_name=b'是否必选'))]