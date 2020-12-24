# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0048_auto_20191226_1413.py
# Compiled at: 2019-12-26 01:13:42
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0047_auto_20191226_1354')]
    operations = [
     migrations.AddField(model_name=b'bargainreward', name=b'bargain_high', field=models.FloatField(blank=True, null=True, verbose_name=b'砍价最高值')),
     migrations.AddField(model_name=b'bargainreward', name=b'bargain_low', field=models.FloatField(blank=True, null=True, verbose_name=b'砍价最低值'))]