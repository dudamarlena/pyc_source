# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0010_auto_20191204_1712.py
# Compiled at: 2019-12-04 04:12:59
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_message', '0009_auto_20191120_1627')]
    operations = [
     migrations.RenameField(model_name=b'weixinserviceaccesstoken', old_name=b'appsecrect', new_name=b'appsecret'),
     migrations.AddField(model_name=b'weixinserviceaccesstoken', name=b'scene', field=models.IntegerField(choices=[(1, '微信服务号'), (2, 'crm砍价小程序')], default=1, verbose_name=b'使用场景'))]