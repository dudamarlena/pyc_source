# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0003_auto_20190129_1620.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0002_auto_20181203_1533')]
    operations = [
     migrations.AlterField(model_name=b'voucher', name=b'expire_at', field=models.DateTimeField(default=datetime.datetime(2219, 1, 29, 16, 20, 55, 692956), verbose_name=b'Expire at'))]