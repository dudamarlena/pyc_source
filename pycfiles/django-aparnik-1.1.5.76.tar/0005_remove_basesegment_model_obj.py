# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0005_remove_basesegment_model_obj.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0004_auto_20181213_1607')]
    operations = [
     migrations.RemoveField(model_name=b'basesegment', name=b'model_obj')]