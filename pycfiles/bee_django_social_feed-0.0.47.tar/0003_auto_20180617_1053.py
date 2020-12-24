# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0003_auto_20180617_1053.py
# Compiled at: 2018-06-16 22:53:11
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0002_feedcomment_created_at')]
    operations = [
     migrations.AddField(model_name=b'feed', name=b'link_link', field=models.CharField(blank=True, max_length=256, null=True, verbose_name=b'链接的http(s)')),
     migrations.AddField(model_name=b'feed', name=b'link_name', field=models.CharField(blank=True, max_length=256, null=True, verbose_name=b'链接显示名称')),
     migrations.AddField(model_name=b'feed', name=b'type', field=models.IntegerField(default=0, verbose_name=b'日志类型'))]