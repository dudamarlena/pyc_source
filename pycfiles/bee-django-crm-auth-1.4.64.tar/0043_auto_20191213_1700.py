# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0043_auto_20191213_1700.py
# Compiled at: 2019-12-13 04:00:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0042_auto_20191212_1436')]
    operations = [
     migrations.AlterModelOptions(name=b'campaignrecord', options={b'ordering': [b'-created_at'], b'permissions': (('view_campaign_record_list', 'view_campaign_record_list'), ('view_campaign_record_detail', 'view_campaign_record_detail'))}),
     migrations.AddField(model_name=b'campaignrecord', name=b'history', field=models.TextField(blank=True, null=True, verbose_name=b'历史记录'))]