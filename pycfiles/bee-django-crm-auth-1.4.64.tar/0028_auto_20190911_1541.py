# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0028_auto_20190911_1541.py
# Compiled at: 2019-09-11 03:41:21
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0027_regcode_course_days')]
    operations = [
     migrations.AlterField(model_name=b'preuser', name=b'mobile', field=models.CharField(max_length=100, verbose_name=b'电话'))]