# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0006_auto_20190131_1436.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0005_auto_20190130_1510')]
    operations = [
     migrations.AlterField(model_name=b'voucher', name=b'expire_at', field=models.DateTimeField(default=datetime.datetime(2300, 10, 5, 18, 0), verbose_name=b'Expire at'))]