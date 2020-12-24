# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0046_auto_20191225_1736.py
# Compiled at: 2019-12-25 04:36:15
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0045_auto_20191220_1903')]
    operations = [
     migrations.AlterField(model_name=b'campaignrecord', name=b'share_qrcode', field=models.ImageField(blank=True, null=True, upload_to=b'bee_django_crm/gift/campaign_record/share_qrcode', verbose_name=b'小程序二维码'))]