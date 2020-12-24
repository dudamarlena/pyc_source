# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0041_auto_20191210_1346.py
# Compiled at: 2019-12-10 00:46:54
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0040_auto_20191206_1705')]
    operations = [
     migrations.AlterUniqueTogether(name=b'bargainrecord', unique_together=set([('campaign_record', 'op_wxuser')])),
     migrations.AlterUniqueTogether(name=b'campaignrecord', unique_together=set([('wxuser', 'reward')]))]