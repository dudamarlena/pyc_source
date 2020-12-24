# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0044_auto_20191220_1754.py
# Compiled at: 2019-12-20 04:54:58
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0043_auto_20191213_1700')]
    operations = [
     migrations.AlterField(model_name=b'campaignrecord', name=b'is_mk', field=models.NullBooleanField(verbose_name=b'是否是老缦客'))]