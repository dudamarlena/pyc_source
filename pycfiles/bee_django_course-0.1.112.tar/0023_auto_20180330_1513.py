# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0023_auto_20180330_1513.py
# Compiled at: 2018-04-01 07:32:39
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0022_sectionvideo')]
    operations = [
     migrations.AlterModelOptions(name=b'course', options={b'ordering': [b'-id'], b'permissions': (('can_choose_course', 'can choose course'), )})]