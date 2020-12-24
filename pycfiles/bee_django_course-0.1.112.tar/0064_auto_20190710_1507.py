# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0064_auto_20190710_1507.py
# Compiled at: 2019-07-10 03:30:18
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0063_auto_20190703_1608')]
    operations = [
     migrations.AlterField(model_name=b'userlive', name=b'provider_name', field=models.CharField(default=b'cc', max_length=180))]