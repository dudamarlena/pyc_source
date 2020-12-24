# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0061_auto_20181221_1443.py
# Compiled at: 2019-03-13 07:53:36
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0060_auto_20181219_1353')]
    operations = [
     migrations.AlterModelOptions(name=b'sectionquestion', options={b'ordering': [b'order_by'], b'permissions': (('view_sectionquestion', '可以查看问题列表'), )})]