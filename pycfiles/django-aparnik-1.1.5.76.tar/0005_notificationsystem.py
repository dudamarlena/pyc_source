# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0005_notificationsystem.py
# Compiled at: 2019-05-17 08:52:49
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0004_auto_20190517_1651')]
    operations = [
     migrations.CreateModel(name=b'NotificationSystem', fields=[], options={b'verbose_name': b'Notification System', 
        b'manager_inheritance_from_future': True, 
        b'proxy': True, 
        b'verbose_name_plural': b'Notifications System', 
        b'indexes': []}, bases=('notifications.notification', ))]