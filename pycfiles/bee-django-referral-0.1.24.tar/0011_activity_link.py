# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0011_activity_link.py
# Compiled at: 2018-08-23 00:30:06
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0010_auto_20180708_1350')]
    operations = [
     migrations.AddField(model_name=b'activity', name=b'link', field=models.URLField(blank=True, help_text=b'填写此字段后，点击后将直接进入第三方页面', max_length=180, null=True, verbose_name=b'跳转链接'))]