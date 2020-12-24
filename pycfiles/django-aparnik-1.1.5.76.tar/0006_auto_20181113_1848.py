# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0006_auto_20181113_1848.py
# Compiled at: 2018-11-13 10:24:14
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('products', '0005_auto_20181108_1132')]
    operations = [
     migrations.RenameField(model_name=b'product', old_name=b'is_free', new_name=b'is_free_field')]