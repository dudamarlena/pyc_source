# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0014_remove_userprofile_is_leave.py
# Compiled at: 2018-10-31 02:34:27
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0013_userprofile_is_leave')]
    operations = [
     migrations.RemoveField(model_name=b'userprofile', name=b'is_leave')]