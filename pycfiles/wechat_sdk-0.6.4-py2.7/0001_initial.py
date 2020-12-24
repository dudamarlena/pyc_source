# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/context/framework/django/migrations/0001_initial.py
# Compiled at: 2014-12-20 23:11:43
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Context', fields=[
      (
       b'openid', models.CharField(max_length=50, serialize=False, verbose_name=b'用户OpenID', primary_key=True)),
      (
       b'context_data', models.TextField(verbose_name=b'上下文对话数据')),
      (
       b'expire_date', models.DateTimeField(verbose_name=b'过期日期', db_index=True))], options={b'db_table': b'wechat_context', 
        b'verbose_name': b'微信上下文对话', 
        b'verbose_name_plural': b'微信上下文对话'}, bases=(
      models.Model,))]