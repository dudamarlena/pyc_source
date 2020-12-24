# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0007_remove_basesegment_sort.py
# Compiled at: 2018-12-13 07:49:53
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0006_basesegment_model_obj')]
    operations = [
     migrations.RemoveField(model_name=b'basesegment', name=b'sort')]