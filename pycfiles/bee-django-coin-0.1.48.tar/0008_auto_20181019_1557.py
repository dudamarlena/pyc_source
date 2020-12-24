# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0008_auto_20181019_1557.py
# Compiled at: 2018-10-19 03:57:43
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0007_auto_20181018_1508')]
    operations = [
     migrations.AlterModelOptions(name=b'othercoincount', options={b'ordering': [b'pk'], b'permissions': (('add_teach_class_coin', '可以发所教班级M币'), )})]