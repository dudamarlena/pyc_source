# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0036_wxuser_avatar_url.py
# Compiled at: 2019-12-02 02:12:43
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0035_auto_20191128_1829')]
    operations = [
     migrations.AddField(model_name=b'wxuser', name=b'avatar_url', field=models.URLField(null=True, verbose_name=b'头像链接'))]