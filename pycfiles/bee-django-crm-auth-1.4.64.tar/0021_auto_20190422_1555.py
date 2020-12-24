# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0021_auto_20190422_1555.py
# Compiled at: 2019-04-22 03:55:33
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0020_regcode_reg_number')]
    operations = [
     migrations.AlterModelOptions(name=b'regcode', options={b'ordering': [b'-pk']}),
     migrations.AlterModelTable(name=b'regcode', table=b'bee_django_crm_code')]