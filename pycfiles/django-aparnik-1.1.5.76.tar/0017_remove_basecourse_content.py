# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0017_remove_basecourse_content.py
# Compiled at: 2019-04-28 08:17:27
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0016_auto_20190428_1646')]
    operations = [
     migrations.RemoveField(model_name=b'basecourse', name=b'content')]