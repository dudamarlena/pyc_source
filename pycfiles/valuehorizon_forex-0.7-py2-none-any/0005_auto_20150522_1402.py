# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0005_auto_20150522_1402.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0004_auto_20150508_1504')]
    operations = [
     migrations.AlterModelOptions(name=b'currency', options={b'ordering': [b'name', b'symbol'], b'verbose_name': b'Currency', b'verbose_name_plural': b'Currencies'})]