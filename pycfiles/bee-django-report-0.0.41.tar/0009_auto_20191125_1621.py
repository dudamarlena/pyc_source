# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0009_auto_20191125_1621.py
# Compiled at: 2019-11-25 03:21:28
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_report', '0008_auto_20191025_1640')]
    operations = [
     migrations.AlterModelOptions(name=b'report', options={b'permissions': (('can_view_report', '可以查看报表'), ('can_view_website_report', 'can_view_website_report'), ('can_view_user_report', 'can_view_user_report'), ('can_view_course_report', 'can_view_course_report'))})]