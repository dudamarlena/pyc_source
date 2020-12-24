# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0055_auto_20200106_1428.py
# Compiled at: 2020-01-06 01:28:24
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0054_customauthpermission')]
    operations = [
     migrations.AlterField(model_name=b'customauthpermission', name=b'app_title', field=models.CharField(max_length=180, null=True, verbose_name=b'应用')),
     migrations.AlterField(model_name=b'customauthpermission', name=b'codename_title', field=models.CharField(max_length=180, null=True, verbose_name=b'权限')),
     migrations.AlterField(model_name=b'customauthpermission', name=b'model_title', field=models.CharField(max_length=180, null=True, verbose_name=b'模块')),
     migrations.AlterField(model_name=b'customauthpermission', name=b'number', field=models.IntegerField(null=True, verbose_name=b'顺序'))]