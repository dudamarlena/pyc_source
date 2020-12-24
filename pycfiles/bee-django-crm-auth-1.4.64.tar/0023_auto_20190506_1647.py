# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0023_auto_20190506_1647.py
# Compiled at: 2019-05-06 04:47:21
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0022_auto_20190422_1925')]
    operations = [
     migrations.AlterModelOptions(name=b'regcode', options={b'ordering': [b'-pk'], b'permissions': (('can_ckeck_code', '可以验证卡密'), ('can_get_code', '可以获取卡密'))})]