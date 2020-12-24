# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0002_auto_20180517_1758.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'applicationquestion', options={b'ordering': [b'order_by'], b'permissions': (('view_crm_application', '可以查看申请表问题列表页'), ), b'verbose_name': b'crm申请表问题'}),
     migrations.AlterModelOptions(name=b'contract', options={b'ordering': [b'-id'], b'permissions': (('view_crm_contract', '可以查看合同'), ), b'verbose_name': b'crm合同'}),
     migrations.AlterModelOptions(name=b'preuser', options={b'ordering': [b'-created_at'], b'permissions': (('can_manage_crm', '可以进入crm管理页'), ('view_crm_preuser', '可以查看crm用户'), ('view_crm_doc', '可以查看帮助文档')), b'verbose_name': b'crm预备用户'}),
     migrations.AlterModelOptions(name=b'preusercontract', options={b'ordering': [b'-paid_at', b'-created_at'], b'permissions': (('view_crm_preuser_contract', '可以查看用户缴费'), ), b'verbose_name': b'crm用户缴费'}),
     migrations.AlterModelOptions(name=b'source', options={b'ordering': [b'-created_at'], b'permissions': (('view_crm_source', '可以查看渠道'), ), b'verbose_name': b'crm渠道'})]