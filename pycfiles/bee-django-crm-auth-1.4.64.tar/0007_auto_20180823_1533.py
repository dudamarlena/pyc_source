# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0007_auto_20180823_1533.py
# Compiled at: 2018-08-23 03:33:17
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0006_auto_20180822_1736')]
    operations = [
     migrations.AlterField(model_name=b'preuserfee', name=b'info', field=models.TextField(blank=True, null=True, verbose_name=b'备注')),
     migrations.AlterField(model_name=b'preuserfee', name=b'pay_status', field=models.IntegerField(choices=[(1, '全款'), (2, '分期头款'), (3, '分期中'), (4, '分期尾款')], default=1, verbose_name=b'付款方式及状态')),
     migrations.AlterField(model_name=b'preuserfee', name=b'study_at', field=models.DateTimeField(blank=True, help_text=b'【全款】及【分期头款】时，此字段必填。其他付款方式可不填写', null=True, verbose_name=b'开课日期'))]