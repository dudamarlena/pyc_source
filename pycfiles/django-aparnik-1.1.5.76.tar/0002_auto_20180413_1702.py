# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/invitation/migrations/0002_auto_20180413_1702.py
# Compiled at: 2018-10-17 07:19:17
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('invitation', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'invite', options={b'verbose_name': b'Invite', b'verbose_name_plural': b'Invites'})]