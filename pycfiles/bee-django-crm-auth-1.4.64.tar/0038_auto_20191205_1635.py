# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0038_auto_20191205_1635.py
# Compiled at: 2019-12-05 03:35:16
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0037_auto_20191202_1930')]
    operations = [
     migrations.AddField(model_name=b'campaignrecord', name=b'share_qrcode', field=models.ImageField(blank=True, null=True, upload_to=b'bee_django_crm/campaign_record/share_qrcode', verbose_name=b'小程序二维码')),
     migrations.AlterField(model_name=b'campaignrecord', name=b'status', field=models.IntegerField(choices=[(1, '进行中'), (2, '已提取'), (3, '已消费')], default=1))]