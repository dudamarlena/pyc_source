# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0050_userleveluprecord_supplement.py
# Compiled at: 2019-11-21 03:10:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0049_auto_20191121_1419')]
    operations = [
     migrations.AddField(model_name=b'userleveluprecord', name=b'supplement', field=models.TextField(blank=True, null=True, verbose_name=b'补充资料'))]