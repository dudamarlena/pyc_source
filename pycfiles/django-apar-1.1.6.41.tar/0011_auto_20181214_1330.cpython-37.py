# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0011_auto_20181214_1330.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 457 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0010_auto_20181205_1107')]
    operations = [
     migrations.RemoveField(model_name='course',
       name='sort'),
     migrations.RemoveField(model_name='coursefile',
       name='sort')]