# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lidayan/pyenv/python3/pypi-distribute/lib/python3.6/site-packages/wxmgmt/migrations/0003_auto_20180210_0834.py
# Compiled at: 2018-02-25 20:14:49
# Size of source mod 2**32: 638 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wxmgmt', '0002_remove_tenant_kefuxinxi')]
    operations = [
     migrations.AlterField(model_name='tenant',
       name='_jsapi_ticket',
       field=models.CharField(blank=True, default='', max_length=200)),
     migrations.AlterField(model_name='tenant',
       name='shanghu_id',
       field=models.CharField(blank=True, default='', help_text='微信支付商户号', max_length=50))]