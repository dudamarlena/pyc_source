# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0013_auto_20180709_1234.py
# Compiled at: 2018-07-09 00:34:47
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0012_auto_20180709_1210')]
    operations = [
     migrations.AlterModelOptions(name=b'album', options={b'ordering': [b'-created_at'], b'permissions': [('can_manage_album', '能进入Albums管理页')]})]