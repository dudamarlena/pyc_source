# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0040_auto_20191018_1358.py
# Compiled at: 2019-10-18 01:58:16
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0039_auto_20191016_1532')]
    operations = [
     migrations.AlterModelOptions(name=b'userleveluprecord', options={b'ordering': [b'-created_at'], b'permissions': (('view_all_level_up_records', '可以查看用户升级列表'), )}),
     migrations.RemoveField(model_name=b'userleveluprecord', name=b'detail'),
     migrations.AddField(model_name=b'userleveluprecord', name=b'application', field=models.TextField(blank=True, null=True, verbose_name=b'申请内容')),
     migrations.AddField(model_name=b'userleveluprecord', name=b'histroy', field=models.TextField(blank=True, null=True, verbose_name=b'历史记录')),
     migrations.AddField(model_name=b'userleveluprecord', name=b'req', field=models.TextField(blank=True, null=True, verbose_name=b'申请要求'))]