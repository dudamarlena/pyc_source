# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/migrations/0002_auto_20141017_0841.py
# Compiled at: 2014-10-17 04:41:22
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_easy_currencies', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'currencyrate', name=b'rate', field=models.DecimalField(max_digits=13, decimal_places=9))]