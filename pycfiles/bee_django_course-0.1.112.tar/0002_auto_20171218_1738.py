# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0002_auto_20171218_1738.py
# Compiled at: 2017-12-18 04:38:41
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'course', options={b'ordering': [b'-id']})]