# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0005_auto_20181016_1619.py
# Compiled at: 2018-10-16 04:19:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0004_auto_20181016_1500')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'expire_date', field=models.DateTimeField(blank=True, null=True, verbose_name=b'结课日期')),
     migrations.AddField(model_name=b'userprofile', name=b'start_date', field=models.DateTimeField(blank=True, null=True, verbose_name=b'开课日期'))]