# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0008_auto_20180706_1627.py
# Compiled at: 2018-07-06 04:27:39
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0007_auto_20180706_1614')]
    operations = [
     migrations.AlterField(model_name=b'activity', name=b'source_id', field=models.IntegerField(blank=True, help_text=b'crm中对应渠道id', null=True, verbose_name=b'渠道id'))]