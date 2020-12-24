# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0085_auto_20200107_1457.py
# Compiled at: 2020-01-07 01:57:43
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0084_auto_20200103_1826')]
    operations = [
     migrations.AlterModelOptions(name=b'sectionattach', options={b'ordering': [b'name']})]