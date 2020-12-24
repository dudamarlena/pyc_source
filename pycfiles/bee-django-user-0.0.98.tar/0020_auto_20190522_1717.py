# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0020_auto_20190522_1717.py
# Compiled at: 2019-05-22 05:17:01
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0019_auto_20190522_1642')]
    operations = [
     migrations.AlterModelOptions(name=b'usersn', options={b'ordering': [b'start']}),
     migrations.AlterModelTable(name=b'usersn', table=b'bee_django_user_sn')]