# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0007_auto_20181018_1508.py
# Compiled at: 2018-10-18 03:08:42
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0006_auto_20181016_1717')]
    operations = [
     migrations.RenameField(model_name=b'othercoincount', old_name=b'other_type_id', new_name=b'coin_content_id')]