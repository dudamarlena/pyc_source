# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0020_regcode_reg_number.py
# Compiled at: 2019-04-22 03:55:17
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0019_regcode_used_preuser')]
    operations = [
     migrations.AddField(model_name=b'regcode', name=b'reg_number', field=models.IntegerField(null=True, unique=True))]