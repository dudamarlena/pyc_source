# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0026_auto_20190711_1718.py
# Compiled at: 2019-07-11 05:18:09
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0025_contract_type')]
    operations = [
     migrations.AlterModelOptions(name=b'source', options={b'ordering': [b'-created_at'], b'permissions': (('view_crm_source', '可以查看渠道'), ('can_change_source_name', '可以修改渠道名称')), b'verbose_name': b'crm渠道'})]