# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0017_auto_20190510_1710.py
# Compiled at: 2019-05-10 05:10:16
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0016_auto_20190510_1652')]
    operations = [
     migrations.AlterField(model_name=b'section', name=b'group_name', field=models.CharField(blank=True, help_text=b'如课件前不需显示，则不用填写', max_length=180, null=True, verbose_name=b'组名'))]