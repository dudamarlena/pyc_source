# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0010_auto_20181205_1107.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 752 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0009_auto_20181105_1424')]
    operations = [
     migrations.AlterModelOptions(name='basecourse',
       options={'verbose_name':'\\u062f\\u0648\\u0631\\u0647 \\u067e\\u0627\\u06cc\\u0647', 
      'verbose_name_plural':'\\u062f\\u0648\\u0631\\u0647 \\u0647\\u0627\\u06cc \\u067e\\u0627\\u06cc\\u0647'}),
     migrations.AlterModelOptions(name='course',
       options={'verbose_name':'\\u062f\\u0648\\u0631\\u0647', 
      'verbose_name_plural':'\\u062f\\u0648\\u0631\\u0647 \\u0647\\u0627'})]