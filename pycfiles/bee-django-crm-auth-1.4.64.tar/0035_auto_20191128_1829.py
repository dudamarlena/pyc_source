# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0035_auto_20191128_1829.py
# Compiled at: 2019-11-28 05:29:30
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0034_auto_20191128_1411')]
    operations = [
     migrations.AlterModelOptions(name=b'bargainrecord', options={b'ordering': [b'-created_at']})]