# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/reusable_app_project/bee_django_course/migrations/0012_remove_section_order_by.py
# Compiled at: 2018-03-19 23:19:54
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0011_auto_20180318_1618')]
    operations = [
     migrations.RemoveField(model_name=b'section', name=b'order_by')]