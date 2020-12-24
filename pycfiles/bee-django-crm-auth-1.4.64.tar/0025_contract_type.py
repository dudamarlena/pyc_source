# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0025_contract_type.py
# Compiled at: 2019-06-29 02:53:46
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0024_auto_20190601_1615')]
    operations = [
     migrations.AddField(model_name=b'contract', name=b'type', field=models.IntegerField(choices=[(1, '普通合同'), (2, '亲子合同')], default=1, verbose_name=b'合同类型'))]