# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0056_coursesectionmid_pionts.py
# Compiled at: 2018-09-17 03:43:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0055_auto_20180914_1626')]
    operations = [
     migrations.AddField(model_name=b'coursesectionmid', name=b'pionts', field=models.IntegerField(default=0, verbose_name=b'通过后获得的M币'))]