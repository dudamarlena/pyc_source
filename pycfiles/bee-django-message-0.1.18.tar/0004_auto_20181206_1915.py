# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0004_auto_20181206_1915.py
# Compiled at: 2018-12-06 06:15:22
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_message', '0003_auto_20181205_2108')]
    operations = [
     migrations.RenameField(model_name=b'message', old_name=b'is_done', new_name=b'need_done'),
     migrations.RenameField(model_name=b'message', old_name=b'is_replay', new_name=b'need_replay'),
     migrations.AlterField(model_name=b'sendrecord', name=b'done_info', field=models.TextField(blank=True, help_text=b'如设置为【发送回执】，填写后会给发送人发站内信', null=True, verbose_name=b'处理结果'))]