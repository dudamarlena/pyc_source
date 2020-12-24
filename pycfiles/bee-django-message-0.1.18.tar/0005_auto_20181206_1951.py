# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0005_auto_20181206_1951.py
# Compiled at: 2018-12-06 06:51:31
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_message', '0004_auto_20181206_1915')]
    operations = [
     migrations.AlterModelOptions(name=b'sendrecord', options={b'ordering': [b'-sent_at'], b'permissions': (('view_message_records', 'Can view message records'), )}),
     migrations.RenameField(model_name=b'message', old_name=b'need_replay', new_name=b'need_reply'),
     migrations.RemoveField(model_name=b'message', name=b'is_admin_show'),
     migrations.RemoveField(model_name=b'message', name=b'is_user_show'),
     migrations.AddField(model_name=b'sendrecord', name=b'done_by', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'done_by_user', to=settings.AUTH_USER_MODEL))]