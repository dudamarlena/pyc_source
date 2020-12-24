# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0023_userexamrecord_status.py
# Compiled at: 2018-03-28 03:58:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0022_auto_20180317_1613')]
    operations = [
     migrations.AddField(model_name=b'userexamrecord', name=b'status', field=models.IntegerField(blank=True, null=True, verbose_name=b'状态'))]