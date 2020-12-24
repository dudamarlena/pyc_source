# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0051_auto_20200108_1535.py
# Compiled at: 2020-01-08 02:35:34
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0050_auto_20200108_1451')]
    operations = [
     migrations.AlterModelOptions(name=b'bargainreward', options={b'ordering': [b'pk'], b'permissions': (('view_bargain_reward_detail', 'view_bargain_reward_detail'), )})]