# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0008_auto_20150526_1310.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forex', '0007_auto_20150526_1255')]
    operations = [
     migrations.AddField(model_name=b'currency', name=b'date_created', field=models.DateTimeField(auto_now_add=True, null=True)),
     migrations.AddField(model_name=b'currency', name=b'date_modified', field=models.DateTimeField(auto_now=True, null=True)),
     migrations.AddField(model_name=b'currencyprices', name=b'date_created', field=models.DateTimeField(auto_now_add=True, null=True)),
     migrations.AddField(model_name=b'currencyprices', name=b'date_modified', field=models.DateTimeField(auto_now=True, null=True))]