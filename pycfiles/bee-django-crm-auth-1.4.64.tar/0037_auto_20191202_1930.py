# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0037_auto_20191202_1930.py
# Compiled at: 2019-12-02 06:30:30
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0036_wxuser_avatar_url')]
    operations = [
     migrations.AddField(model_name=b'bargainrecord', name=b'wx_avatar_url', field=models.URLField(null=True, verbose_name=b'头像链接')),
     migrations.AddField(model_name=b'bargainrecord', name=b'wx_nickname', field=models.CharField(max_length=180, null=True, verbose_name=b'微信昵称')),
     migrations.AlterField(model_name=b'wxuser', name=b'user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]