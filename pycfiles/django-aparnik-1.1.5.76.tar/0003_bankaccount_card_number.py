# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/bankaccounts/migrations/0003_bankaccount_card_number.py
# Compiled at: 2019-03-15 09:51:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bankaccounts', '0002_auto_20190215_1916')]
    operations = [
     migrations.AddField(model_name=b'bankaccount', name=b'card_number', field=models.CharField(default=b'1111111111111111', max_length=16, verbose_name=b'Card Number'), preserve_default=False)]