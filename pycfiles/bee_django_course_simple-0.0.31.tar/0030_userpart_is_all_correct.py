# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0030_userpart_is_all_correct.py
# Compiled at: 2019-11-06 02:45:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0029_auto_20191106_1409')]
    operations = [
     migrations.AddField(model_name=b'userpart', name=b'is_all_correct', field=models.BooleanField(default=False, verbose_name=b'是否全对'))]