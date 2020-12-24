# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0036_userprofile_live_mins.py
# Compiled at: 2019-10-10 03:18:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0035_auto_20190923_1715')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'live_mins', field=models.IntegerField(default=0, verbose_name=b'直播时长'))]