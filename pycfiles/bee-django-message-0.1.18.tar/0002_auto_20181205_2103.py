# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0002_auto_20181205_2103.py
# Compiled at: 2018-12-05 08:03:21
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_message', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'message', name=b'is_done', field=models.BooleanField(default=False, help_text=b'如果不需后台显示，则不用填写', verbose_name=b'是否需要后台处理')),
     migrations.AddField(model_name=b'message', name=b'is_replay', field=models.BooleanField(default=False, help_text=b'如果不需处理，则不用填写', verbose_name=b'后台处理后是否回复')),
     migrations.AddField(model_name=b'sendrecord', name=b'done_at', field=models.DateTimeField(null=True)),
     migrations.AddField(model_name=b'sendrecord', name=b'done_info', field=models.TextField(blank=True, null=True, verbose_name=b'处理结果')),
     migrations.AddField(model_name=b'sendrecord', name=b'is_done', field=models.BooleanField(default=False, verbose_name=b'是否处理过'))]