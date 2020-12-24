# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0002_cointype_identity.py
# Compiled at: 2018-04-10 06:23:19
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'cointype', name=b'identity', field=models.CharField(max_length=180, null=True, unique=True, verbose_name=b'标识符'))]