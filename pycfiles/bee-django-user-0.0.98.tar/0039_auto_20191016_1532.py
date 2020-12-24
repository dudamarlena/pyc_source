# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0039_auto_20191016_1532.py
# Compiled at: 2019-10-16 03:32:07
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     ('bee_django_user', '0038_userlevel_userleveluprecord')]
    operations = [
     migrations.RemoveField(model_name=b'userlevel', name=b'after_group'),
     migrations.AddField(model_name=b'userlevel', name=b'after_group', field=models.ForeignKey(help_text=b'（不可多选）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'user_after_group', to=b'auth.Group', verbose_name=b'升级后的用户组'))]