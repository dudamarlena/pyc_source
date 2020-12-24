# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0007_auto_20190501_1147.py
# Compiled at: 2019-05-01 03:17:29
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0006_auto_20190501_1142')]
    operations = [
     migrations.RemoveField(model_name=b'file', name=b'iv'),
     migrations.RemoveField(model_name=b'file', name=b'password')]