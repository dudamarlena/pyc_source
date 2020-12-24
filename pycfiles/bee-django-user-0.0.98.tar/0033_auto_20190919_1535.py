# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0033_auto_20190919_1535.py
# Compiled at: 2019-09-19 03:35:44
from __future__ import unicode_literals
import datetime
from django.db import migrations, models
from django.utils.timezone import utc

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0032_userclass_lecturer')]
    operations = [
     migrations.AlterField(model_name=b'userleaverecord', name=b'created_at', field=models.DateTimeField(default=datetime.datetime(2019, 9, 19, 7, 35, 43, 378032, tzinfo=utc)))]