# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0023_userprofile_wxapp_openid.py
# Compiled at: 2019-06-21 10:22:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0022_auto_20190612_1746')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'wxapp_openid', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'微信小程序open id'))]