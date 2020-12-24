# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0021_auto_20190523_1602.py
# Compiled at: 2019-05-23 04:02:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0020_auto_20190522_1717')]
    operations = [
     migrations.AlterField(model_name=b'userprofile', name=b'sn', field=models.IntegerField(help_text=b'只需填写数字', null=True, unique=True, verbose_name=b'统一缦客号'))]