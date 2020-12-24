# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/bankaccounts/migrations/0002_auto_20190215_1916.py
# Compiled at: 2019-02-15 10:47:13
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bankaccounts', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'bankaccount', name=b'shaba_number', field=models.CharField(max_length=255, unique=True, verbose_name=b'Shaba Number'))]