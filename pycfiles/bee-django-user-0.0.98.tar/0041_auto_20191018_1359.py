# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0041_auto_20191018_1359.py
# Compiled at: 2019-10-18 01:59:35
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0040_auto_20191018_1358')]
    operations = [
     migrations.RenameField(model_name=b'userlevel', old_name=b'detail', new_name=b'req'),
     migrations.RemoveField(model_name=b'userleveluprecord', name=b'req')]