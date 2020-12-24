# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0004_auto_20190517_1651.py
# Compiled at: 2019-05-17 08:21:54
from __future__ import unicode_literals
import aparnik.contrib.notifications.models
from django.db import migrations
import django_enumfield.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0003_auto_20190517_1651')]
    operations = [
     migrations.RemoveField(model_name=b'notification', name=b'is_for_all_users'),
     migrations.AlterField(model_name=b'notification', name=b'notification_send_type', field=django_enumfield.db.fields.EnumField(default=2, enum=aparnik.contrib.notifications.models.NotificationType, verbose_name=b'Notification send type'))]