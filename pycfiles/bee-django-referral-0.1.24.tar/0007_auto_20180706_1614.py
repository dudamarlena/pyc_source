# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0007_auto_20180706_1614.py
# Compiled at: 2018-07-06 04:14:24
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0006_auto_20180706_1552')]
    operations = [
     migrations.AddField(model_name=b'activity', name=b'link_name', field=models.CharField(default=b'a', max_length=180, verbose_name=b'链接文字'), preserve_default=False),
     migrations.AlterField(model_name=b'activity', name=b'source_id', field=models.IntegerField(blank=True, null=True, verbose_name=b'渠道id')),
     migrations.AlterField(model_name=b'useractivity', name=b'activity', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_referral.Activity', verbose_name=b'转介活动'))]